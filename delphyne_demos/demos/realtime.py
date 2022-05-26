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
Manipulating the rate of time at startup and in runtime.
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


class RealtimeRateChanger(object):

    """Simple class that hooks to the simulation callback and dynamically
    changes the real-time rate"""

    def __init__(self, initial_steps):
        self._steps = initial_steps

    def tick(self, behaviour_tree):
        """Process simulation step"""
        if self._steps == 0:
            last_round_realtime_rate = behaviour_tree.runner.get_stats(
            ).get_current_realtime_rate()
            rate = behaviour_tree.runner.get_realtime_rate() + 0.2
            if rate >= 1.6:
                rate = 0.6
            self._steps = int(rate * 400)
            behaviour_tree.runner.set_realtime_rate(rate)
            print("Running at real-time rate {0} for {1} steps."
                  " Last real-time measure was {2}"
                  .format(rate, self._steps, last_round_realtime_rate))
        else:
            self._steps -= 1


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        "Realtime Rate Changer",
        """
This example shows how the real-time simulation rate can be set both when the
simulator runner is created and while the simulation is running.

To pass an initial real-time rate use the `--realtime_rate` flag, like:

$ {0} --realtime_rate=2.0

If none is specified the default will be set to `1.0` (i.e. run the simulation
in real-time).

Once the scripts starts running it will cycle between a real-time rate of `0.6`
to `1.6` to depict how dynamic real-time rate impacts on the simulation.
        """.format(os.path.basename(sys.argv[0])))
    return parser.parse_args()


def create_realtime_scenario_subtree():
    scenario_subtree = delphyne.behaviours.roads.Road()
    scenario_subtree.add_child(
        delphyne.behaviours.agents.SimpleCar(name=str(0), speed=0.0))
    return scenario_subtree

##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    # Read the initial real-time rate from command line. Default to 1.0 if none
    # specified.
    args = parse_arguments()

    # Since this is the first time the simulator runs we compensate for the
    # startup time by running it 2 times longer than the dynamically changing
    # loop.
    initial_steps = int(args.realtime_rate * 800)
    rate_changer = RealtimeRateChanger(initial_steps)

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_realtime_scenario_subtree())

    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        log=args.log,
        logfile_name=args.logfile_name
    )

    simulation_tree.add_post_tick_handler(rate_changer.tick)

    print("Running at real-time rate {0} for {1} steps"
          .format(simulation_tree.runner.get_realtime_rate(), initial_steps))

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
