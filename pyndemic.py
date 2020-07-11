#!/usr/bin/env python3
import sys

from pyndemic.controller import GameController
from pyndemic.ui import ConsoleUI


def main(args):
    random_state = int(args[0]) if args else None

    controller = GameController(random_state=random_state)
    ui = ConsoleUI(controller=controller)

    ui.run()


if __name__ == '__main__':
    cli_args = sys.argv[1:]
    main(cli_args)
