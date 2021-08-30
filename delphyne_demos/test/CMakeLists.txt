# TODO(francocipollone): Improve this check by wrapping add_test() function.
# When sanitizers are activated python scripts are disabled.
if (NOT ${SANITIZERS})
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
    NAME smoke_test_delphyne_gazoo
    COMMAND ${PROJECT_SOURCE_DIR}/examples/delphyne_gazoo -b -d 2
  )
endif()
