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
A keyop demo.
"""
##############################################################################
# Imports
##############################################################################

import delphyne.trees
import delphyne.behaviours

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers
from . import keyboard_handler

##############################################################################
# Supporting Classes & Methods
##############################################################################


def demo_callback(behaviour_tree, keyboard_handler, time_step_seconds):
    """Callback function invoqued by the SimulationRunner
    at every time step.
    """
    if keyboard_handler.key_hit():
        key = keyboard_handler.get_character().lower()
        if key == 'p':
            if behaviour_tree.runner.is_simulation_paused():
                behaviour_tree.runner.unpause_simulation()
                print("Simulation is now running.")
            else:
                behaviour_tree.runner.pause_simulation()
                print("Simulation is now paused.")
        elif key == 'q':
            behaviour_tree.interrupt()
            print("Quitting simulation.")
        elif key == 's':
            if behaviour_tree.runner.is_simulation_paused():
                behaviour_tree.runner.request_simulation_step_execution(1)
                print("Simulation step of {0}s executed.".
                      format(time_step_seconds))
            else:
                print("Simulation step only supported in paused mode.")


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        "Keyboard Teleoperation & Time Manipulation",
        """
This example shows how to use the keyboard events to control the
advance of a simulation. The simulation will open the usual simple
car in the center of the scene, which can be driven using the
keyboard on the GUI's teleop widget. In the console, we can toggle
(p) play/pause, (s) step and (q) quit the simulation.
        """
        )
    return parser.parse_args()


def create_scenario_subtree():
    scenario_subtree = delphyne.behaviours.roads.Road()
    scenario_subtree.add_child(
        delphyne.behaviours.agents.SimpleCar(
            name='0',
            speed=0.0))
    return scenario_subtree

##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_scenario_subtree())

    sim_runner_time_step = 0.01
    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        logfile_name=args.logfile_name,
        log=args.log,
        time_step=sim_runner_time_step
    )

    keyboard = keyboard_handler.get_keyboard_handler()

    # We add it as a step callback because the runner
    # gets stuck in a while loop until it's unpaused.
    # See simulation_runner.cc line 185 at delphyne's repository.
    simulation_tree.runner.add_step_callback(
        lambda: demo_callback(simulation_tree, keyboard,
                              sim_runner_time_step))

    print("\n"
          "************************************************************\n"
          "* Instructions for running the demo:                       *\n"
          "* <p> will pause the simulation if unpaused and viceversa. *\n"
          "* <s> will step the simulation once if paused.             *\n"
          "* <q> will stop the simulation and quit the demo.          *\n"
          "************************************************************\n")

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
