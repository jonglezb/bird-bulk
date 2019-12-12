#!/usr/bin/env python3

import socket
import sys

import bird_cli


SOCKET_PATH = "/var/run/bird/bird.ctl"


def connect(socket_path):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(socket_path)
    # Read banner
    banner = bird_cli.parse_reply(sock)
    print("Connected to daemon:", banner[0][1].decode())
    return sock

def benchmark(sock, n=1000):
    """Send [n] route queries and discard replies"""
    for i in range(n):
        bird_cli.send_message(sock, "show route for 8.8.8.8 all")
        bird_cli.parse_reply(sock)


if __name__ == '__main__':
    s = connect(SOCKET_PATH)
    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])
        benchmark(s, iterations)
    else:
        benchmark(s)
