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
The dragway demo.
"""
##############################################################################
# Imports
##############################################################################

import delphyne.trees
import delphyne.behaviours

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers

##############################################################################
# Supporting Classes & Methods
##############################################################################


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        "Dragway",
        "\nAll of delphyne's agents on a single dragway.\n",
        default_duration=15.0)
    return parser.parse_args()


def create_dragway_scenario_subtree():
    scenario_subtree = delphyne.behaviours.roads.Dragway(
        name="dragway",
        num_lanes=5,
        length=100.0,
        lane_width=3.7,
        shoulder_width=3.0,
        maximum_height=5.0
    )
    scenario_subtree.add_children([
        delphyne.behaviours.agents.SimpleCar(
            name='simple-car',
            initial_pose=(0.0, 1.5 * 3.7, 0.)
        ),
        delphyne.behaviours.agents.MobilCar(
            name='mobil-car',
            initial_pose=(0.0, -0.5 * 3.7, 0.0),
            speed=1.0
        ),
        delphyne.behaviours.agents.RailCar(
            name='rail-car',
            lane_id='Dragway_Lane_1',
            longitudinal_position=0.0,
            lateral_offset=0.0,
            speed=3.0
        ),
        delphyne.behaviours.agents.TrajectoryAgent(
            name='trajectory-car',
            times=[0.0, 5.0, 10.0, 15.0, 20.0],
            headings=[0.0, 0.0, 0.0, 0.0, 0.0],
            waypoints=[
                [0.0,   -5.55, 0.0],  # noqa: E241
                [10.0,  -5.55, 0.0],  # noqa: E241
                [30.0,  -5.55, 0.0],  # noqa: E241
                [60.0,  -5.55, 0.0],  # noqa: E241
                [100.0, -5.55, 0.0]
            ]
        ),
        delphyne.behaviours.agents.UnicycleCar(
            name='unicycle-car',
            initial_pose=(0.0, 3.0 * 3.7, 0.)
        )
    ])

    return scenario_subtree


##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_dragway_scenario_subtree()
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
