[![gcc](https://github.com/ToyotaResearchInstitute/delphyne_demos/actions/workflows/build.yml/badge.svg)](https://github.com/ToyotaResearchInstitute/delphyne_demos/actions/workflows/build.yml)

# delphyne_demos

This is the repository for Delphyne demos, a front-end visualizer for `delphyne`.

## Build

1. Setup a development workspace as described [here](https://github.com/ToyotaResearchInstitute/maliput_documentation/blob/main/docs/installation_quickstart.rst).

2. Build Delphyne packages and their dependencies:

  - If not building drake from source:

   ```sh
   colcon build --packages-up-to delphyne_demos
   ```

  - If building drake from source:

   ```sh
   colcon build --cmake-args -DWITH_PYTHON_VERSION=3 --packages-up-to delphyne_demos
   ```

   **Note**: To build documentation a `-BUILD_DOCS` cmake flag is required:
   ```sh
   colcon build --packages-up-to delphyne_demos --cmake-args " -DBUILD_DOCS=On"
   ```

## Tools

An automated script that looks for all C++ source files and calls `clang-format` accordingly:

```sh
./delphyne_demos/tools/reformat_code.sh
```

This script must be run from the top-level of the repository in order to find all of the files.
It is recommended to run this before opening any pull request.
