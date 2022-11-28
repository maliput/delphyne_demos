#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, Woven Planet. All rights reserved.
# Copyright (c) 2017-2022, Toyota Research Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
The gazoo demo.
"""

##############################################################################
# Imports
##############################################################################


import os.path
from dataclasses import dataclass
from enum import Enum

import delphyne.behaviours
import delphyne.trees
import delphyne_gui.utilities

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers

##############################################################################
# Supporting Classes & Methods
##############################################################################


class MaliputBackend(Enum):
    MALIPUT_MULTILANE = "maliput_multilane"
    MALIPUT_OSM = "maliput_osm"


def get_maliput_osm_circuit():
    """Resolve the path for the circuit map against maliput_osm resources root location."""
    root = delphyne.utilities.get_from_env_or_fail('MALIPUT_OSM_RESOURCE_ROOT')
    filename = "circuit.osm"
    for root in root.split(':'):
        resolved_path = os.path.join(root, 'resources', 'osm', filename)
        if os.path.exists(resolved_path):
            return resolved_path
    return ''


def get_delphyne_gui_circuit():
    """Resolve the path for the circuit map against delphyne_gui resources root location."""
    filename = "roads/circuit.yaml"
    resolved_path = delphyne_gui.utilities.get_delphyne_gui_resource(filename)
    if os.path.exists(resolved_path):
        return resolved_path
    return ''


@dataclass
class ScenarioSubtreeConfig:
    """Configuration for the scenario subtree."""
    name: str
    circuit_filepath: str
    lanes: list
    origin: str = "{0., 0.}"


def get_scenario_subtree_config(backend):
    """Obtain the circuit filepath based on the selected backend."""
    if MaliputBackend(backend) == MaliputBackend.MALIPUT_MULTILANE:
        config = ScenarioSubtreeConfig(name="circuit_multilane",
                                       circuit_filepath=get_delphyne_gui_circuit(),
                                       lanes=["l:s1_0", "l:s1_1", "l:s1_2"])
    elif(MaliputBackend(backend) == MaliputBackend.MALIPUT_OSM):
        config = ScenarioSubtreeConfig(name="circuit_osm",
                                       circuit_filepath=get_maliput_osm_circuit(),
                                       lanes=["1825", "1405", "1352"],
                                       origin="{0., 0.}")
    else:
        print("Backend {} not supported".format(backend))
        quit()
    return config


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        "Gazoo Racing!",
        """
An example of three railcars and a variable number of MOBIL controlled
cars running in a closed-loop maliput road.

See also https://toyotagazooracing.com/
        """
    )
    parser.add_argument("-n", "--num-cars", default=3, type=int,
                        help="The number of MOBIL cars on scene (default: 3).")

    parser.add_argument("-m", "--maliput-backend", default="maliput_multilane", type=str,
                        help="""The maliput backend to use, maliput_osm or maliput_multilane
                        (default: maliput_multilane).""")

    return parser.parse_args()


def add_agents_to_scenario(scenario_subtree, mobil_cars_num, lanes):
    "Adds agents to the scenario subtree."
    # Setup railcar 1
    railcar_speed = 4.0  # (m/s)
    railcar_s = 0.0      # (m)
    robot_id = 1
    lane_1 = lanes[0]
    scenario_subtree.add_child(
        delphyne.behaviours.agents.RailCar(
            name=str(robot_id),
            lane_id=lane_1,
            longitudinal_position=railcar_s,
            lateral_offset=0.0,
            speed=railcar_speed
        )
    )

    # Setup railcar 2
    railcar_speed = 8.0  # (m/s)
    railcar_s = 0.0      # (m)
    robot_id += 1
    lane_2 = lanes[1]
    scenario_subtree.add_child(
        delphyne.behaviours.agents.RailCar(
            name=str(robot_id),
            lane_id=lane_2,
            longitudinal_position=railcar_s,
            lateral_offset=0.0,
            speed=railcar_speed
        )
    )

    # Setup railcar 3
    railcar_speed = 7.0  # (m/s)
    railcar_s = 0.0      # (m)
    robot_id += 1
    lane_3 = lanes[2]
    scenario_subtree.add_child(
        delphyne.behaviours.agents.RailCar(
            name=str(robot_id),
            lane_id=lane_3,
            longitudinal_position=railcar_s,
            lateral_offset=0.0,
            speed=railcar_speed
        )
    )

    # Setup MOBIL cars.
    for i in range(mobil_cars_num):
        x_offset = 5.0       # (m)
        y_offset = 5.0       # (m)
        velocity_base = 2.0  # (m/s)
        robot_id += 1
        scenario_subtree.add_child(
            delphyne.behaviours.agents.MobilCar(
                name=str(robot_id),
                initial_pose=(
                    -10.0 + x_offset * (1 + i / 3),
                    0.0 + y_offset * (i % 3),
                    0.0
                ),
                speed=velocity_base * i
            )
        )

    return scenario_subtree


def create_gazoo_scenario_subtree(backend, mobil_cars_num):
    "Creates the Gazoo scenario subtree."
    print("Creating Gazoo scenario subtree...")
    config = get_scenario_subtree_config(backend)
    if not os.path.isfile(config.circuit_filepath):
        print("Required map 'circuit' not found for the backend: {}"
              .format(backend))
        quit()
    features = delphyne.roads.ObjFeatures()
    features.draw_elevation_bounds = False
    if(MaliputBackend(backend) == MaliputBackend.MALIPUT_MULTILANE):
        scenario_subtree = delphyne.behaviours.roads.Multilane(
            file_path=config.circuit_filepath,
            name=config.name,
            features=features,

        )
    elif(MaliputBackend(backend) == MaliputBackend.MALIPUT_OSM):
        scenario_subtree = delphyne.behaviours.roads.MaliputOSM(
            file_path=config.circuit_filepath,
            name=config.name,
            origin=config.origin,
            features=features
        )
    else:
        print("Backend {} not supported".format(backend))
        quit()

    return add_agents_to_scenario(scenario_subtree, mobil_cars_num, config.lanes)


##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    if args.num_cars > 6 or args.num_cars < 0:
        print("The number of cars must be in the range of 0 to 6.")
        quit()

    mobil_cars_num = args.num_cars
    maliput_backend = args.maliput_backend

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_gazoo_scenario_subtree(maliput_backend, mobil_cars_num)
    )

    sim_runner_time_step = 0.015
    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        log=args.log,
        logfile_name=args.logfile_name,
        time_step=sim_runner_time_step
    )

    tree_time_step = 0.03
    with launch_interactive_simulation(
        simulation_tree.runner, layout=args.layout, bare=args.bare, ign_visualizer="visualizer"
    ) as launcher:
        if args.duration < 0:
            # run indefinitely
            print("Running simulation indefinitely.")
            simulation_tree.tick_tock(period=tree_time_step)
        else:
            # run for a finite time
            print("Running simulation for {0} seconds.".format(args.duration))
            simulation_tree.tick_tock(
                period=tree_time_step, number_of_iterations=int(args.duration / tree_time_step)
            )
        launcher.terminate()
