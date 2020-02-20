#!/usr/bin/env python3

import time
import sys
import re

from bird_cli import BirdCLI

#Choose the suitable socket for IPv4 or IPv6 queries
v4_socket = "/var/run/bird/bird.ctl"
v6_socket = "/var/run/bird/bird6.ctl"

def benchmark(cli, stdin):
    for i in stdin:
        i = i.rstrip()

        errors = []
        flag = False

        reply = []
        
        while not reply:
            
            #if BrokenPipeError exception, reconnect and sleep
            snd_msg = False
            while not snd_msg:
                snd_msg = cli.send_message("show route for " + i + " all")
                if not snd_msg:
                    time.sleep(0.01)

            reply = cli.parse_reply()
            
            #if could not connect to Bird, reconnect and sleep
            if not reply:
                time.sleep(0.01)

        for j in reply:
            #if route path was returned, write it to stdout
            if (j[0].decode("utf-8") == "1012"):
                as_path = re.search(r'BGP.as_path: (.*)', j[1].decode("utf-8")).group(1)
                print("{}\t{}".format(i, as_path))
                flag = True
                break
            else:
                errors.append(j)
        if flag:
            continue
        else:
            #if route path was not returned, collect all the error messages and display them
            errors = [item for sublist in errors for item in sublist]
            errors = [i.decode("utf-8") for i in errors]
            print("{}\tErrors: {}".format(i,", ".join(errors)))

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: {} v[4,6]".format(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == "v6":
        cli = BirdCLI(socket_path=v6_socket)
    elif sys.argv[1] == "v4":
        cli = BirdCLI(socket_path=v4_socket)
    else:
        print("Usage: {} v[4,6]".format(sys.argv[0]))
        sys.exit(1)

    cli.parse_reply()[0]
    benchmark(cli, sys.stdin)
