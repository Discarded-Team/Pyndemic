# coding: utf-8
from abc import ABCMeta, abstractmethod
import logging


class InputManager(metaclass=ABCMeta):
    @abstractmethod
    def input(self):
        pass


class ConsoleInputManager(InputManager):
    def __init__(self, input_mode='stream', input_file=None):
        self.input_mode = input_mode
        self.input_file = input_file

        if self.input_mode == 'file':
            if input_file is None:
                raise ValueError('You must specify `input_file` argument if '
                                 '`input_mode` is "file".')
            with open(self.input_file, 'r') as fin:
                self.cached_commands = fin.readlines()
            self.cached_commands.reverse()

    def input(self):
        if self.input_mode == 'file':
            try:
                command = self.cached_commands.pop().rstrip()
            except IndexError:
                self.input_mode = 'stream'
                logging.warning(
                    'No more commands in cached input! Now switching to manual mode.')
        if self.input_mode == 'stream':
            command = input()

        return command


class FileInputManager(InputManager):
    def __init__(self, input_mode='stream', input_file=None):
        self.input_mode = input_mode
        self.input_file = input_file

        if self.input_mode == 'file':
            if input_file is None:
                raise ValueError('You must specify `input_file` argument if '
                                 '`input_mode` is "file".')
            with open(self.input_file, 'r') as fin:
                self.cached_commands = fin.readlines()
            self.cached_commands.reverse()

