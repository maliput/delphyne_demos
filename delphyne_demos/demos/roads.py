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
Load a simulation with one of a few sample maliput road networks.
"""
##############################################################################
# Imports
##############################################################################

import os
import sys

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
        "Maliput Roads",
        """
Load one of the various types of maliput road networks
into an empty (free of agents) simulation. For the time
being the following road network types are supported:
dragway, onramp, and multilane.

This demo uses the subcommand style, where each road
type can handle different parameters.

The optional arguments that are common to all the roads
should be located before the road type.

$ {0} --help

To get help on each
road type's parameters, run for example:

$ {0} multilane --help

Some examples:

$ {0} dragway --length=200 --shoulder-width=2.5
$ {0} onramp
$ {0} multilane
--filename='./install/share/delphyne/roads/circuit.yaml'
$ {0} malidrive
--filename='./install/share/delphyne/roads/circuit.xodr'
--name=my_circuit
        """.format(os.path.basename(sys.argv[0]))
    )
    subparsers = parser.add_subparsers(dest="road_type")

    # Dragway subcommand
    dragway_parser = subparsers.add_parser("dragway")
    dragway_parser.add_argument("--lanes", default=3,
                                type=int,
                                help="the number of lanes the dragway has")
    dragway_parser.add_argument("--length", default=100.0,
                                type=float,
                                help="the length of the dragway, in meters")
    dragway_parser.add_argument("--lane-width", default=3.7,
                                type=float,
                                help="the width of each lane, in meters")
    dragway_parser.add_argument("--shoulder-width", default=1.0,
                                type=float,
                                help="the width of the road shoulder,\
                                in meters")
    dragway_parser.add_argument("--max-height", default=5.0,
                                type=float,
                                help="the maximum allowed height for the road,\
                                in meters")

    # Onramp subcommand
    subparsers.add_parser("onramp")

    # Multilane subcommand
    multilane_parser = subparsers.add_parser("multilane")
    multilane_parser.add_argument("--filename",
                                  help="multilane file path",
                                  required=True)

    # Malidrive subcommand
    malidrive_parser = subparsers.add_parser("malidrive")
    malidrive_parser.add_argument("--filename",
                                  help="malidrive file path",
                                  required=True)
    malidrive_parser.add_argument("--name",
                                  help="malidrive road name",
                                  default="maliroad")

    return parser.parse_args()

##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    if args.road_type == "dragway":
        scenario_subtree = delphyne.behaviours.roads.Dragway(
            name="Demo Dragway",
            num_lanes=args.lanes,
            length=args.length,
            lane_width=args.lane_width,
            shoulder_width=args.shoulder_width,
            maximum_height=args.max_height)
    elif args.road_type == "onramp":
        scenario_subtree = delphyne.behaviours.roads.OnRamp()
    elif args.road_type == "multilane":
        scenario_subtree = delphyne.behaviours.roads.Multilane(
            file_path=args.filename)
    elif args.road_type == "malidrive":
        scenario_subtree = delphyne.behaviours.roads.Malidrive(
            file_path=args.filename,
            name=args.name)
    else:
        print("Option {} not recognized".format(args.road_type))
        sys.exit()

    simulation_tree = delphyne.trees.BehaviourTree(
        root=scenario_subtree)

    try:
        simulation_tree.setup(
            realtime_rate=args.realtime_rate,
            start_paused=args.paused,
            log=args.log,
            logfile_name=args.logfile_name
        )
    except RuntimeError as error:
        print("An error ocurred while trying to run the simulation with : {}".format(args.filename))
        print(str(error))
        print("Exiting the simulation")
        sys.exit()

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
