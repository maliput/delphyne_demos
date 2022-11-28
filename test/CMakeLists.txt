# TODO(francocipollone): Improve this check by wrapping add_test() function.
# When sanitizers are activated python scripts are disabled.
if (NOT ${SANITIZERS})
  ## delphyne_mali_osm
  add_test(
    NAME smoke_test_delphyne_mali_osm_straight_forward
    COMMAND delphyne_mali_osm -n StraightForward -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_arc_lane
    COMMAND delphyne_mali_osm -n ArcLane -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_arc_lane_dense
    COMMAND delphyne_mali_osm -n ArcLaneDense -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_elevated_arc_lane_dense
    COMMAND delphyne_mali_osm -n ElevatedArcLane -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_c_shape_superelevated_road
    COMMAND delphyne_mali_osm -n CShapeSuperelevatedRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_l_shape_road
    COMMAND delphyne_mali_osm -n LShapeRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_y_shape_road
    COMMAND delphyne_mali_osm -n YShapeRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_t_shape_road
    COMMAND delphyne_mali_osm -n TShapeRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_osm_circuit
    COMMAND delphyne_mali_osm -n Circuit -b -d 2
  )

  ## delphyne_mali
  add_test(
    NAME smoke_test_delphyne_mali_line_single_lane
    COMMAND delphyne_mali -n LineSingleLane -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_arc_single_lane
    COMMAND delphyne_mali -n ArcSingleLane -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_s_shape_road
    COMMAND delphyne_mali -n SShapeRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_l_shape_road
    COMMAND delphyne_mali -n LShapeRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_l_shape_road_variable_lanes
    COMMAND delphyne_mali -n LShapeRoadVariableLanes -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_t_shape_road
    COMMAND delphyne_mali -n TShapeRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_line_multiple_sections
    COMMAND delphyne_mali -n LineMultipleSections -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_flat_town_01
    COMMAND delphyne_mali -n FlatTown01 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_parking_garage_ramp
    COMMAND delphyne_mali -n ParkingGarageRamp -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_s_shape_superelevated_road
    COMMAND delphyne_mali -n SShapeSuperelevatedRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_r_r_long_road
    COMMAND delphyne_mali -n RRLongRoad -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_highway
    COMMAND delphyne_mali -n Highway -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_variable_width
    COMMAND delphyne_mali -n LineVariableWidth -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_figure_8
    COMMAND delphyne_mali -n Figure8 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_r_r_figure_8
    COMMAND delphyne_mali -n RRFigure8 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_01
    COMMAND delphyne_mali -n Town01 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_02
    COMMAND delphyne_mali -n Town02 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_03
    COMMAND delphyne_mali -n Town03 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_04
    COMMAND delphyne_mali -n Town04 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_05
    COMMAND delphyne_mali -n Town05 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_06
    COMMAND delphyne_mali -n Town06 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_town_07
    COMMAND delphyne_mali -n Town07 -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_variable_offset
    COMMAND delphyne_mali -n LineVariableOffset -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_single_road_pedestrian_crosswalk
    COMMAND delphyne_mali -n SingleRoadPedestrianCrosswalk -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mali_loop_road_pedestrian_crosswalk
    COMMAND delphyne_mali -n LoopRoadPedestrianCrosswalk -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_gazoo
    COMMAND delphyne_gazoo -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_gazoo_osm
    COMMAND delphyne_gazoo -m maliput_osm -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_city
    COMMAND delphyne_city -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_crash
    COMMAND delphyne_crash -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_dragway
    COMMAND delphyne_dragway -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_keyop
    COMMAND delphyne_keyop -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_mobil_perf
    COMMAND delphyne_mobil_perf curved_lanes -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_realtime
    COMMAND delphyne_realtime -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_roads
    COMMAND delphyne_roads -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_scriptlets
    COMMAND delphyne_scriptlets -b -d 2
  )
  add_test(
    NAME smoke_test_delphyne_trip_integration
    COMMAND delphyne_trip_integration -b -d 2
  )
endif()
