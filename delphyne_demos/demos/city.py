#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, Woven Planet. All rights reserved.
# Copyright (c) 2018-2022, Toyota Research Institute. All rights reserved.
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
The city demo.

"""
##############################################################################
# Imports
##############################################################################

import functools
import os.path
import sys

import delphyne.trees
import delphyne.behaviours
import delphyne.blackboard
import delphyne.maliput as maliput

import delphyne_gui.utilities

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers

##############################################################################
# Supporting Classes & Methods
##############################################################################


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        "City traffic",
        """
An example of city traffic with a variable number of railcars and
MOBIL controlled cars running in a closed-loop maliput road.
        """
    )
    parser.add_argument(
        "-n", "--num-rail-cars", default=40, type=int,
        help="The number of rails cars on scene (default: 40)."
    )
    parser.add_argument(
        "-m", "--num-mobil-cars", default=10, type=int,
        help="The number of MOBIL cars on scene (default: 10)."
    )

    return parser.parse_args()

##############################################################################
# Main
##############################################################################


def lane_position_to_inertial_pose2d(road_geometry, lane_id, lane_position):

    from delphyne.blackboard.providers import resolve
    lane_id = resolve(lane_id, road_geometry)
    lane_position = resolve(lane_position, road_geometry, lane_id)

    road_index = road_geometry.ById()
    lane = road_index.GetLane(maliput.LaneId(lane_id))
    inertial_position = lane.ToInertialPosition(lane_position)
    inertial_orientation = lane.GetOrientation(lane_position)
    xyz = inertial_position.xyz()
    initial_heading = inertial_orientation.rpy().yaw_angle()
    return xyz.x(), xyz.y(), initial_heading


def create_city_scenario_subtree(num_rail_cars, num_mobil_cars):
    file_path = delphyne_gui.utilities.get_delphyne_gui_resource(
        "roads/little_city.yaml"
    )

    if not os.path.isfile(file_path):
        print("Required file {} not found."
              " Please, make sure to install the latest delphyne_gui."
              .format(os.path.abspath(file_path)))
        sys.exit()

    scenario_subtree = delphyne.behaviours.roads.Multilane(
        file_path=file_path, name="little_city"
    )

    provider = delphyne.blackboard.providers.LaneLocationProvider(
        distance_between_agents=6.0, seed=1
    )

    # Sets up all railcars.
    for n in range(num_rail_cars):
        scenario_subtree.add_child(
            delphyne.behaviours.agents.RailCar(
                name='rail{}'.format(n),
                lane_id=provider.random_lane,
                longitudinal_position=0.0,
                lateral_offset=0.0,
                speed=4.0
            )
        )

    # Sets up all MOBIL cars.
    mobilcar_speed = 4.0  # (m/s)
    for m in range(num_mobil_cars):
        scenario_subtree.add_child(
            delphyne.behaviours.agents.MobilCar(
                name='mobil{}'.format(m),
                speed=mobilcar_speed,
                initial_pose=functools.partial(
                    lane_position_to_inertial_pose2d,
                    lane_id=provider.random_lane,
                    lane_position=provider.random_lane_position
                )
            )
        )

    return scenario_subtree


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_city_scenario_subtree(
            args.num_rail_cars, args.num_mobil_cars
        )
    )

    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        log=args.log,
        logfile_name=args.logfile_name
    )

    tree_time_step = 0.02
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
