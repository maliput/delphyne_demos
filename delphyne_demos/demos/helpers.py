#!/usr/bin/env python3

# BSD 3-Clause License
#
# Copyright (c) 2022, Woven Planet. All rights reserved.
# Copyright (c) 2017-2022, Toyota Research Institute. All rights reserved.
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

##############################################################################
# Documentation
##############################################################################

"""Utility methods for the demos."""

##############################################################################
# Imports
##############################################################################

import argparse

import delphyne.cmdline as cmdline

##############################################################################
# Argument parsing
##############################################################################


def create_argument_parser(title, content, default_duration=-1.0):
    """
    Create an argument parser for use with the demos and
    populate it with some common arguments.
    Args:
        title: short, descriptive title for the demo
        content: longer, detailed description of the demo
        default_duration: default length of the simulation (s)
    Returns:
        argparse.ArgParser: the initialised argument parser
    """

    def check_positive_float_or_zero(value):
        """Check that the passed argument is a positive float value"""
        float_value = float(value)
        if float_value < 0.0:
            raise argparse.ArgumentTypeError("%s is not a positive float value"
                                             % value)
        return float_value

    parser = argparse.ArgumentParser(
        description=cmdline.create_argparse_description(title, content),
        epilog=cmdline.create_argparse_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--duration", type=float,
                        default=default_duration,
                        help="Simulation length (sec)(endless if -ve)"
                        "(default: {0}s)".format(default_duration))
    parser.add_argument("-r", "--realtime_rate", default=1.0,
                        type=check_positive_float_or_zero,
                        help="Ratio of sim vs real time (default: 1.0)")
    parser.add_argument('-p', '--paused',
                        action='store_true',
                        help='Start the simulation paused (default: False)')
    parser.add_argument('-l', '--log',
                        action='store_true',
                        help='Log simulation data (default: False)')
    parser.add_argument('-f', '--logfile_name', default="",
                        action='store', type=str,
                        help='Custom logfile name (default: empty string)')
    parser.add_argument('-b', '--bare', action='store_true',
                        default=False, help=('Run simulation with no '
                                             'visualizer (default: False)'))
    parser.add_argument('-y', '--layout', default="layout_with_teleop.config",
                        action='store', type=str,
                        help='Custom layout config file path.'
                             'If the path is relative it will look for it '
                             'first at env `DELPHYNE_GUI_RESOURCE_ROOT/layouts` '
                             'location and then at the execution location. '
                             '(default: layout_with_teleop.config)')
    return parser
