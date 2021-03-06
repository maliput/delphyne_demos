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
The crash demo.
"""
##############################################################################
# Imports
##############################################################################

import math
import numpy as np

import delphyne.trees
import delphyne.behaviours

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers

##############################################################################
# Supporting Classes & Methods
##############################################################################


def parse_arguments():
    """Argument passing and demo documentation."""
    parser = helpers.create_argument_parser(
        "Car Crash!",
        """
An example that exercises collision detection by setting up multiple cars
in collision course.
        """
    )
    return parser.parse_args()


def check_for_agent_collisions(simulation_subtree):
    """
    Pre tick handler that checks for collisions between agents in simulation.

    TODO(hidmic): make it a behaviour?
    """
    simulation = simulation_subtree.runner.get_simulation()
    agent_collisions = simulation.get_collisions()
    if not agent_collisions:
        return
    print("Collisions have been detected!")
    for collision in agent_collisions:
        agent1, agent2 = collision.agents
        print("\n{} and {} have crashed at {}!".format(
            agent1.name(), agent2.name(), collision.location
        ))
        agent1_velocity = agent1.get_velocity()
        print("--> {} was going at {} m/s and hit {}.".format(
            agent1.name(), np.linalg.norm(agent1_velocity[3:]), agent2.name()
        ))
        print("    It now rests at {}.".format(agent1.get_pose_translation()))
        agent2_velocity = agent2.get_velocity()
        print("--> {} was going at {} m/s and hit {}.".format(
            agent2.name(), np.linalg.norm(agent2_velocity[3:]), agent1.name()
        ))
        print("    It now rests at {}.".format(agent2.get_pose_translation()))
    simulation_subtree.runner.pause_simulation()
    print("\nSimulation paused.")


def create_crash_scenario_subtree():
    scenario_subtree = delphyne.behaviours.roads.Road()

    scenario_subtree.add_children([
        delphyne.behaviours.agents.SimpleCar(
            name="racer0",
            # scene coordinates (m, m, radians)
            initial_pose=(0.0, -50.0, math.pi/2),
            # speed in the direction of travel (m/s)
            speed=5.0
        ),
        delphyne.behaviours.agents.SimpleCar(
            name="racer1",
            # scene coordinates (m, m, radians)
            initial_pose=(-50.0, 0.0, 0.),
            # speed in the direction of travel (m/s)
            speed=5.1
        ),
        delphyne.behaviours.agents.SimpleCar(
            name="racer2",
            # scene coordinates (m, m, radians)
            initial_pose=(0.0, 50.0, -math.pi/2),
            # speed in the direction of travel (m/s)
            speed=5.0
        ),
        delphyne.behaviours.agents.SimpleCar(
            name="racer3",
            # scene coordinates (m, m, radians)
            initial_pose=(50.0, 0.0, math.pi),
            # speed in the direction of travel (m/s)
            speed=5.1
        ),
    ])

    return scenario_subtree


##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_crash_scenario_subtree()
    )

    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        log=args.log,
        logfile_name=args.logfile_name
    )

    # Adds a callback to check for agent collisions.
    simulation_tree.add_pre_tick_handler(check_for_agent_collisions)

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
