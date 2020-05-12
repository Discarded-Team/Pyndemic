#!/usr/bin/env python3
# coding: utf-8
import sys

from src.controller import GameController


__version__ = "0.1.0"


def main(args):
    default_stdin = sys.stdin

    input_file = args[0] if args else None
    random_state = int(args[1]) if args[1:] else None

    if input_file:
        sys.stdin = open(input_file, 'r')
    controller = GameController(random_state)
    controller.run()

    while True:
        try:
            command = sys.stdin.readline().rstrip()
        except EOFError:
            sys.stdin = default_stdin
            continue
        except KeyboardInterrupt:
            print('You decided to exit the game...')
            command = 'quit'

        response = controller.send(command)
        print(response)

        if response['type'] == 'termination':
            break


if __name__ == '__main__':
    cli_args = sys.argv[1:]
    main(cli_args)
