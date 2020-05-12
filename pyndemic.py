#!/usr/bin/env python3
# coding: utf-8
import sys

from src.controller import GameController
from src.ui import ConsoleUI

__version__ = "0.1.0"


def main(args):
    random_state = int(args[0]) if args else None

    controller = GameController(random_state=random_state)
    ui = ConsoleUI(controller=controller)

    ui.run()


if __name__ == '__main__':
    cli_args = sys.argv[1:]
    main(cli_args)
