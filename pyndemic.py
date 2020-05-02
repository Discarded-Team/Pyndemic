#!/usr/bin/env python3
# coding: utf-8
import sys

from src.controller import MainController


__version__ = "0.1.0"


if __name__ == '__main__':
    cli_args = sys.argv[1:]

    input_file = cli_args[0] if cli_args else None
    random_state = int(cli_args[1]) if cli_args[1:] else None

    controller = MainController(input_file, random_state)
    controller.run()

