##############################################################################
# Scripts
##############################################################################

# TODO(daniel.stonier) if we ever have other executables that are not demos
# consider renaming these to delphyne_demo_<name>

install(
  PROGRAMS
    delphyne_city
    delphyne_crash
    delphyne_dragway
    delphyne_gazoo
    delphyne_keyop
    delphyne_mali
    delphyne_mali_osm
    delphyne_mobil_perf
    delphyne_realtime
    delphyne_roads
    delphyne_scriptlets
    delphyne_trip_integration
  DESTINATION
    bin
)
