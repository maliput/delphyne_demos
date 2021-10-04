#!/usr/bin/env python3
#
# Copyright 2021 Toyota Research Institute
#
##############################################################################
# Documentation
##############################################################################

"""Keyboard handler for the demos."""

##############################################################################
# Imports
##############################################################################

import atexit
import sys
import termios

from abc import ABC, abstractmethod
from select import select


class KeyboardHandler(ABC):
    """Interface to handle keyboard interaction."""

    @abstractmethod
    def key_hit(self):
        """Returns True when a key is hit"""
        pass

    @abstractmethod
    def get_character(self):
        """Returns the pressed character from the keyboard"""
        pass


class KeyboardStdIn(KeyboardHandler):
    """A keyboard-interrupt poller. Allows users to read a keyboard
    input with a non-locking behavior making use of the select function,
    available on most *nix systems.

    This class is based on the work done by Frank Deng, available on GitHub
    as part of a set of python tools released under the MIT licence:
    https://github.com/frank-deng/experimental-works/blob/master/kbhit.py .
    """

    def __init__(self):
        self.input_stream = sys.stdin
        # Save current terminal settings
        self.file_descriptor = self.input_stream.fileno()
        self.new_terminal = termios.tcgetattr(self.file_descriptor)
        self.old_terminal = termios.tcgetattr(self.file_descriptor)
        # New terminal setting unbuffered
        self.new_terminal[3] = (self.new_terminal[3] &
                                ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.file_descriptor,
                          termios.TCSAFLUSH, self.new_terminal)
        # Support normal-terminal reset at exit
        atexit.register(self._set_normal_term)

    def _set_normal_term(self):
        """Resets to default terminal settings."""
        termios.tcsetattr(self.file_descriptor,
                          termios.TCSAFLUSH, self.old_terminal)

    def get_character(self):
        """Reads a character from the keyboard."""
        char = self.input_stream.read(1)
        if char == '\x00' or ord(char) >= 0xA1:
            return char + self.input_stream.read(1)
        return char

    def key_hit(self):
        """Returns True if a keyboard key has been pressed, False otherwise."""
        key_hit, _, _ = select([self.input_stream], [], [], 0)
        return key_hit != []


class KeyboardStub(KeyboardHandler):
    """Stub implementation of a KeyboardHandler.
    Typically used for non-interactive applications where no stdin is available."""
    def key_hit(self):
        return False

    def get_character(self):
        return None


def get_keyboard_handler() -> KeyboardHandler:
    """Returns a KeyboardHandler implementation based on sys.stdin.isatty() result."""
    if sys.stdin.isatty():
        return KeyboardStdIn()
    else:
        return KeyboardStub()
