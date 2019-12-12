#!/usr/bin/env python3

import sys

from bird_cli import BirdCLI


def benchmark(cli, n=1000):
    """Send [n] route queries and discard replies"""
    for i in range(n):
        cli.send_message("show route for 8.8.8.8 all")
        cli.parse_reply()


if __name__ == '__main__':
    cli = BirdCLI()
    (code, banner, _) = cli.parse_message()
    print("Connected to daemon:", banner.decode())
    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])
        benchmark(cli, iterations)
    else:
        benchmark(cli)
