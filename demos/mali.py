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
The maliput_malidrive demo.
```
"""
##############################################################################
# Imports
##############################################################################

import os.path

import delphyne.trees
import delphyne.behaviours
import delphyne.blackboard.providers
import delphyne.roads as delphyne_roads
import delphyne.utilities as utilities

from delphyne_gui.utilities import launch_interactive_simulation

from . import helpers

##############################################################################
# Supporting Classes & Methods
##############################################################################

KNOWN_ROADS = {
    'LineSingleLane': {
        'description': 'Single line lane of 100m length',
        'file_path': 'odr/SingleLane.xodr',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'ArcSingleLane': {
        'description': ('Single arc lane of 100m length '
                        'and 40m of radius'),
        'file_path': 'odr/ArcLane.xodr',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'SShapeRoad': {
        'description': ('Single lane describing a S shape road.'),
        'file_path': 'odr/SShapeRoad.xodr',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'LShapeRoad': {
        'description': ('Single lane describing a L shape road.'),
        'file_path': 'odr/LShapeRoad.xodr',
        'lane_id': '1_0_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'LShapeRoadVariableLanes': {
        'description': ('Variable number of lanes describing a L shape road.'),
        'file_path': 'odr/LShapeRoadVariableLanes.xodr',
        'lane_id': '1_0_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'TShapeRoad': {
        'description': 'T intersection road with double hand roads',
        'lane_id': '2_0_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'LineMultipleSections': {
        'description': ('A single flat road with multiple LaneSections.'),
        'file_path': 'odr/LineMultipleSections.xodr',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'FlatTown01': {
        'description': 'Flat grid city',
        'lane_id': '25_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'ParkingGarageRamp': {
        'description': ('A pitched road curve describing a parking garage ramp.'),
        'file_path': 'odr/ParkingGarageRamp.xodr',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'SShapeSuperelevatedRoad': {
        'description': 'Multiple lanes describing a S shape road with superelevation',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'RRLongRoad': {
        'description': 'Long road with turning lanes',
        'file_path': 'odr/RRLongRoad.xodr',
        'lane_id': '0_0_-4',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'Highway': {
        'description': 'Highway',
        'lane_id': '1_0_2',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'LineVariableWidth': {
        'description': 'Straight Road with variable width',
        'lane_id': '1_0_2',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'Figure8': {
        'description': '8-shaped road ',
        'lane_id': '1_0_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'RRFigure8': {
        'description': '8-shaped road ',
        'lane_id': '1_0_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 3e-1,
        'angular_tolerance': 3e-1,
    },
    'Town01': {
        'description': 'Grid city',
        'lane_id': '25_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'Town02': {
        'description': 'Grid city',
        'lane_id': '1_0_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'Town03': {
        'description': 'Grid city',
        'lane_id': '352_1_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 2e-1,
    },
    'Town04': {
        'description': 'Grid city',
        'lane_id': '735_0_-4',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 7e-2,
    },
    'Town05': {
        'description': 'Grid city',
        'lane_id': '3_0_2',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'Town06': {
        'description': 'Grid city',
        'lane_id': '75_0_3',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'Town07': {
        'description': 'Grid city',
        'lane_id': '438_1_1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'LineVariableOffset': {
        'description': 'Straight Road with varying offset',
        'lane_id': '1_0_2',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 5e-2,
    },
    'SingleRoadPedestrianCrosswalk': {
        'description': 'Single line with a virtual pedestrian crosswalk',
        'file_path': 'odr/SingleRoadPedestrianCrosswalk.xodr',
        'yaml_file_path': 'odr/SingleRoadPedestrianCrosswalk.yaml',
        'agent_type': 'RuleRailCar',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'LoopRoadPedestrianCrosswalk': {
        'description': 'Loop with two virtual pedestrian crosswalks',
        'file_path': 'odr/LoopRoadPedestrianCrosswalk.xodr',
        'yaml_file_path': 'odr/LoopRoadPedestrianCrosswalk.yaml',
        'agent_type': 'RuleRailCar',
        'lane_id': '1_0_-1',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
}


def parse_arguments():
    "Argument passing and demo documentation."
    parser = helpers.create_argument_parser(
        'Mali Racing!',
        """
An example of a railcar running in an OpenDrive based maliput road.
        """
    )

    argument_help = """\
The OpenDRIVE road description to drive on. Either a path
to an .xodr file or one of the following well known roads: {}.
All relative paths are resolved against MALIPUT_MALIDRIVE_RESOURCE_ROOT if not
found in the current working directory.
""".format(', '.join(KNOWN_ROADS))

    parser.add_argument(
        '-n', '--road_name', default='SShapeRoad', help=argument_help
    )

    parser.add_argument(
        '-yn', '--yaml_name', default='', help=argument_help
    )

    parser.add_argument(
        '-lt', '--linear_tolerance', default='1e-3', help=argument_help
    )

    parser.add_argument(
        '-at', '--agent_type', default='RailCar', help=argument_help
    )
    return parser.parse_args()


def get_malidrive_resource(path):
    """Resolve the path against malidrive resources root location."""
    root = utilities.get_from_env_or_fail('MALIPUT_MALIDRIVE_RESOURCE_ROOT')
    for root in root.split(':'):
        resolved_path = os.path.join(root, 'resources', path)
        if os.path.exists(resolved_path):
            return resolved_path
    return ''


def create_mali_scenario_subtree(file_path, yaml_file_path, features,
                                 lane_position, agent_type, direction_of_travel,
                                 lane_id, linear_tolerance,
                                 angular_tolerance=1e-3):
    scenario_subtree = delphyne.behaviours.roads.Malidrive(
        file_path=file_path,
        rule_registry_file_path=yaml_file_path,
        road_rulebook_file_path=yaml_file_path,
        traffic_light_book_path=yaml_file_path,
        phase_ring_path=yaml_file_path,
        intersection_book_path=yaml_file_path,
        name=os.path.splitext(os.path.basename(file_path))[0],
        features=features,
        linear_tolerance=linear_tolerance,
        angular_tolerance=angular_tolerance,
    )

    if agent_type == 'RuleRailCar':
        scenario_subtree.add_child(
            delphyne.behaviours.agents.RuleRailCar(
                name='rule-rail-car',
                lane_id=lane_id,
                longitudinal_position=lane_position,
                lateral_offset=0.,
                speed=15.0,
                direction_of_travel=direction_of_travel
            )
        )
    else:
        scenario_subtree.add_child(
            delphyne.behaviours.agents.RailCar(
                name='rail-car',
                lane_id=lane_id,
                longitudinal_position=lane_position,
                lateral_offset=0.,
                speed=15.0,
                direction_of_travel=direction_of_travel
            )
        )
    return scenario_subtree

##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    if os.path.isfile(args.road_name):
        road = {
            'description': 'Custom user-provided road',
            'file_path': args.road_name,
            'yaml_file_path': args.yaml_name,
            'linear_tolerance': args.linear_tolerance,
            'agent_type': args.agent_type,
            'lane_position': 0.,
            'moving_forward': True,
        }
    elif args.road_name in KNOWN_ROADS:
        road = KNOWN_ROADS[args.road_name]
        if 'file_path' not in road:
            road['file_path'] = os.path.join(
                'odr', args.road_name + '.xodr'
            )
        if 'yaml_file_path' not in road:
            road['yaml_file_path'] = os.path.join(
                'odr', args.yaml_name + '.yaml'
            )
        if not os.path.isabs(road['file_path']):
            road['file_path'] = get_malidrive_resource(road['file_path'])
        if not os.path.isabs(road['yaml_file_path']):
            road['yaml_file_path'] = get_malidrive_resource(road['yaml_file_path'])
        if 'agent_type' not in road:
            road['agent_type'] = "RailCar"
    else:
        print("Unknown road {}.".format(args.road_name))
        quit()

    if 'lane_id' in road:
        lane_id = road['lane_id']
    else:
        lane_provider =                                                                    \
            delphyne.blackboard.providers.LaneLocationProvider(distance_between_agents=1.0)
        lane_id = lane_provider.random_lane

    features = delphyne_roads.ObjFeatures()
    features.draw_arrows = True
    features.draw_elevation_bounds = False
    features.draw_stripes = True
    features.draw_lane_haze = False
    features.draw_branch_points = False

    angular_tolerance = 1e-3 if 'angular_tolerance' not in road else road['angular_tolerance']
    simulation_tree = delphyne.trees.BehaviourTree(
        root=create_mali_scenario_subtree(road['file_path'], road['yaml_file_path'], features,
                                          road['lane_position'], road['agent_type'],
                                          road['moving_forward'], lane_id,
                                          road['linear_tolerance'],
                                          angular_tolerance=angular_tolerance))

    sim_runner_time_step = 0.015
    simulation_tree.setup(
        realtime_rate=args.realtime_rate,
        start_paused=args.paused,
        logfile_name=args.logfile_name,
        log=args.log,
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
