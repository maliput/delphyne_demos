##############################################################################
# Modules
##############################################################################

install(
  FILES
    __init__.py
    city.py
    crash.py
    dragway.py
    helpers.py
    gazoo.py
    keyboard_handler.py
    keyop.py
    mali.py
    mali_osm.py
    mobil_perf.py
    realtime.py
    roads.py
    scriptlets.py
    trip_integration.py
  DESTINATION
    ${PYTHON_INSTALL_DIR}/delphyne_demos/demos
)
