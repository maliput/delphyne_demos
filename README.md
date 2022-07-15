[![GCC](https://github.com/maliput/delphyne_demos/actions/workflows/build.yml/badge.svg)](https://github.com/maliput/delphyne_demos/actions/workflows/build.yml)

# delphyne_demos

## Description
This packages provides integration examples for the [`delphyne`](https://github.com/maliput/delphyne) framework.

[![GCC](https://github.com/maliput/delphyne_gui/actions/workflows/build.yml/badge.svg)](https://github.com/maliput/delphyne_gui/actions/workflows/build.yml)


## Demos

These examples are intended to demonstrate how to use `delphyne` from the python layer. Each script permits the `--help` argument which provides a more detailed explanation of the example's functionality and purpose.

They are located at the [examples](examples) folder.

### Try them

After installing `delphyne_demos` simply run a executable, e.g:
```sh
delphyne_gazoo
```
or
```sh
delphyne_mali
```

## Installation

### Supported platforms

Ubuntu Focal Fossa 20.04 LTS.

### Source Installation on Ubuntu

#### Prerequisites

```
sudo apt install python3-rosdep python3-colcon-common-extensions
```

#### Build

1. Create colcon workspace if you don't have one yet.
    ```sh
    mkdir colcon_ws/src -p
    ```

2. Clone dependencies in the `src` folder
    ```sh
    cd colcon_ws/src
    git clone https://github.com/maliput/drake_vendor.git
    ```
    ```
    git clone https://github.com/maliput/delphyne.git
    ```
    ```
    git clone https://github.com/maliput/delphyne_gui.git
    ```

3. Clone this repository in the `src` folder
    ```sh
    cd colcon_ws/src
    git clone https://github.com/maliput/delphyne_demos.git
    ```

4. Install package dependencies via `rosdep`
    ```
    export ROS_DISTRO=foxy
    ```
    ```sh
    rosdep update
    rosdep install -i -y --rosdistro $ROS_DISTRO --from-paths src
    ```
5. Follow instructions to install drake via [`drake_vendor`](https://github.com/maliput/drake_vendor) package.

6. Build the package
    ```sh
    colcon build --packages-up-to delphyne_demos
    ```

For further info refer to [Source Installation on Ubuntu](https://maliput.readthedocs.io/en/latest/installation.html#source-installation-on-ubuntu)

### For development

It is recommended to follow the guidelines for setting up a development workspace as described [here](https://maliput.readthedocs.io/en/latest/developer_setup.html).

## Contributing

Please see [CONTRIBUTING](https://maliput.readthedocs.io/en/latest/contributing.html) page.

## License

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/maliput/delphyne_demos/blob/main/LICENSE)
