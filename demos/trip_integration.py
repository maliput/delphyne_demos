#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, Woven Planet. All rights reserved.
# Copyright (c) 2020-2022, Toyota Research Institute. All rights reserved.
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
A simple keyop demo for integrating with the portable agent framework (TRIP).
"""
##############################################################################
# Imports
##############################################################################

import delphyne.trees
import delphyne.behaviours
import py_trees.behaviour
import py_trees.common

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers
from . import keyboard_handler


##############################################################################
# Supporting Classes & Methods
##############################################################################


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        "Keyboard teleop demo of a car with no physical constraints",
        """
A simple demo for operating a very basic car obeying no phystical
constraints whatsoever.  The purpose is to demonstrate basic usage
for further integration and as a starting point for integration with
other agent modeling frameworks.  The car can be operated using the
<i>-<k>-<j>-<l> keys.
        """
        )
    return parser.parse_args()


class KeyopAccelerateSteerUnicycleCar(py_trees.behaviour.Behaviour):
    """A class for operating the UnicycleCar agent via keyboard commands.
    """

    def __init__(self, agent_name, keyboard_handler, name=py_trees.common.Name.AUTO_GENERATED):
        super().__init__(name)
        self.keyboard_handler = keyboard_handler
        self.acceleration = 0.0
        self.angular_rate = 0.0
        self.agent_name = agent_name

    def initialise(self):
        self.status = py_trees.common.Status.RUNNING

    def late_setup(self, simulation):
        self.simulation = simulation
        self.agent = simulation.get_agent_by_name(self.agent_name)
        self.agent.set_acceleration(self.acceleration)
        self.agent.set_angular_rate(self.angular_rate)

    def update(self):
        if self.keyboard_handler.key_hit():
            key = self.keyboard_handler.get_character().lower()
            if key == 'i':
                print("Accelerate!")
                self.acceleration += 0.1
            if key == 'k':
                print("Decelerate!")
                self.acceleration -= 0.1
            if key == 'j':
                print("Steer Left!")
                self.angular_rate += 0.01
            if key == 'l':
                print("Steer Right!")
                self.angular_rate -= 0.01
        self.agent.set_acceleration(self.acceleration)
        self.agent.set_angular_rate(self.angular_rate)
        self.status = py_trees.common.Status.SUCCESS
        return self.status


def create_scenario_subtree(keyboard):
    scenario_subtree = delphyne.behaviours.roads.Road()
    scenario_subtree.add_children([
        delphyne.behaviours.agents.UnicycleCar(
            name='unicycle_agent',
            speed=0.0),
        KeyopAccelerateSteerUnicycleCar(
            agent_name='unicycle_agent',
            keyboard_handler=keyboard),
    ])
    return scenario_subtree


##############################################################################
# Main
##############################################################################

def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    time_step = 0.01  # The timestep of the simulation and tree.

    keyboard = keyboard_handler.get_keyboard_handler()

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_scenario_subtree(keyboard))

    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        log=args.log,
        logfile_name=args.logfile_name,
        time_step=time_step
    )

    print("\n"
          "************************************************************\n"
          "* A simple demo for operating a very basic car obeying no  *\n"
          "* phystical constraints whatsoever.                        *\n"
          "* Instructions for running the demo:                       *\n"
          "* <i> accelerates the car.                                 *\n"
          "* <k> decelerates the car.                                 *\n"
          "* <j> increase the angular rate to the left.               *\n"
          "* <l> increase the angular rate to the right.              *\n"
          "* CTRL-C to exit.                                          *\n"
          "************************************************************\n")

    with launch_interactive_simulation(
            simulation_tree.runner, layout=args.layout, bare=args.bare
    ) as launcher:
        if args.duration < 0:
            # run indefinitely
            print("Running simulation indefinitely.")
            simulation_tree.tick_tock(period=time_step)
        else:
            # run for a finite time
            print("Running simulation for {0} seconds.".format(args.duration))
            simulation_tree.tick_tock(
                period=time_step, number_of_iterations=int(args.duration / time_step)
            )
        launcher.terminate()
