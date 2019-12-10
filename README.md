# Bird bulk query tool

The goal of this tool is to query the Bird routing daemon with a high volume
of query.

We use a persistent connection to the local Unix socket to be efficient.

## How to use

For now it's simply a benchmark that calls `show route for 8.8.8.8 all` many times
and discards the output from Bird.  The number of iterations is passed as argument:

    python3 birdbulk.py 100000

On a machine with a full BGP view (782383 routes), it takes 5.6 seconds, which means
a query rate of around 18k queries per second.
