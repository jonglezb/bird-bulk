# Bird bulk query tool

The goal of this tool is to help query the Bird routing daemon with a high volume
of queries.

The library is written in Python 3 and uses a persistent connection to the local Unix
socket to be efficient.

## Benchmark

For now the only application is a simple benchmark that calls `show route for 8.8.8.8 all` many times
and discards the replies received from Bird.  The number of iterations is passed as argument:

    python3 benchmark.py 100000

On a machine with a full BGP view (782642 routes), it takes around 6 seconds, which means
a query rate of around 17k queries per second.
