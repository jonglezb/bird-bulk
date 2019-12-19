#!/usr/bin/env python3

import sys

from bird_cli import BirdCLI

MSG = "show route for 8.8.8.8 all"

def benchmark(cli, n):
    """Send [n] route queries and discard replies"""
    for i in range(n):
        cli.send_message(MSG)
        cli.parse_reply()


if __name__ == '__main__':
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    print("Bird CLI benchmark.")
    print("usage: {} [nb_iterations]".format(sys.argv[0]))
    cli = BirdCLI()
    (code, banner) = cli.parse_reply()[0]
    print("Connected to daemon:", banner.decode())
    print("Now sending {} times the query '{}' in a loop...".format(iterations, MSG))
    benchmark(cli, iterations)
