#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, Woven Planet.
# All rights reserved.
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
The maliput_osm demo.
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
    'StraightForward': {
        'description': 'Single line lane of 1000m length',
        'file_path': 'straight_forward.osm',
        'origin': '{0., 0.}',
        'lane_id': '1010',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'ArcLane': {
        'description': 'Arc-shaped road of 100m length',
        'file_path': 'arc_lane.osm',
        'origin': '{0., 0.}',
        'lane_id': '1068',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'ArcLaneDense': {
        'description': 'Arc-shaped road of 100m length with a high sampling resolution.',
        'file_path': 'arc_lane_dense.osm',
        'origin': '{0., 0.}',
        'lane_id': '3985',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'ElevatedArcLane': {
        'description': 'Arc-shaped road with an increasing elevation',
        'file_path': 'elevated_arc_lane.osm',
        'origin': '{0., 0.}',
        'lane_id': '1191',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'CShapeSuperelevatedRoad': {
        'description': 'C-shaped road with an variation in superelevation',
        'file_path': 'c_shape_superelevated_road.osm',
        'origin': '{0., 0.}',
        'lane_id': '1498',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'LShapeRoad': {
        'description': 'L-shaped road.',
        'file_path': 'l_shape_road.osm',
        'origin': '{0., 0.}',
        'lane_id': '1206',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'YShapeRoad': {
        'description': 'Y-shaped road.',
        'file_path': 'y_shape_road.osm',
        'origin': '{0., 0.}',
        'lane_id': '1336',
        'lane_position': 46.,
        'moving_forward': False,
        'linear_tolerance': 1e-3,
    },
    'TShapeRoad': {
        'description': 'T-shaped road.',
        'file_path': 't_shape_road.osm',
        'origin': '{0., 0.}',
        'lane_id': '1830',
        'lane_position': 0.,
        'moving_forward': True,
        'linear_tolerance': 1e-3,
    },
    'Circuit': {
        'description': 'A circuit map.',
        'file_path': 'circuit.osm',
        'origin': '{0., 0.}',
        'lane_id': '2158',
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
An example of a railcar running in an lanelet2 based osm map format.
        """
    )

    argument_help = """\
The OpenDRIVE road description to drive on. Either a path
to an .xodr file or one of the following well known roads: {}.
All relative paths are resolved against MALIPUT_OSM_RESOURCE_ROOT if not
found in the current working directory.
""".format(', '.join(KNOWN_ROADS))

    parser.add_argument(
        '-n', '--road_name', default='StraightForward', help=argument_help
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


def get_maliput_osm_resource(path):
    """Resolve the path against maliput_osm resources root location."""
    root = utilities.get_from_env_or_fail('MALIPUT_OSM_RESOURCE_ROOT')
    for root in root.split(':'):
        resolved_path = os.path.join(root, 'resources', 'osm', path)
        if os.path.exists(resolved_path):
            return resolved_path
    return ''


def create_mali_scenario_subtree(file_path, origin, yaml_file_path, features,
                                 lane_position, agent_type, direction_of_travel,
                                 lane_id, linear_tolerance,
                                 angular_tolerance=1e-3):
    scenario_subtree = delphyne.behaviours.roads.MaliputOSM(
        file_path=file_path,
        origin=origin,
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


def get_road_configuration(args):
    """Return the configuration given the arguments of the application."""
    if os.path.isfile(args.road_name):
        road = {
            'description': 'Custom user-provided road',
            'file_path': args.road_name,
            'origin': args.origin,
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
        if 'origin' not in road:
            road['origin'] = '{0, 0, 0}'
        if 'yaml_file_path' not in road:
            road['yaml_file_path'] = os.path.join(
                'odr', args.yaml_name + '.yaml'
            )
        if not os.path.isabs(road['file_path']):
            road['file_path'] = get_maliput_osm_resource(road['file_path'])
        if not os.path.isabs(road['yaml_file_path']):
            road['yaml_file_path'] = get_maliput_osm_resource(road['yaml_file_path'])
        if 'agent_type' not in road:
            road['agent_type'] = "RailCar"
    else:
        print("Unknown road {}.".format(args.road_name))
        quit()
    return road

##############################################################################
# Main
##############################################################################


def main():
    """Keeping pylint entertained."""
    args = parse_arguments()

    road = get_road_configuration(args)

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
        root=create_mali_scenario_subtree(road['file_path'], road['origin'],
                                          road['yaml_file_path'], features,
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
