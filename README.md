memcached test
--------------

Small repos with some testing scripts that attempt to profile the latency of
making memcached requests with various python libraries.  The key/value pairs in
data.json are all small strings (uuids), so this is not a test of throughput or
even perhaps real world performance if you are storing large objects.

method
------

3 libraries are tested standalone (in a serial method) and under gevent which
attempts to use a greenpool to parallelize 2, 4, 8, and 16 ways.  Running
`test.py` will run all tests and update this file with the results.

results
-------

pylibmc: sync
Write for 25000 keys: 1.32s, 18908.06/s (0.000 avg, 0.000 min, 0.002 max)
Read for  25000 keys: 1.09s, 18908.06/s (0.000 avg, 0.000 min, 0.004 max)


pylibmc: gevent-16
Write 25000 keys: 2.13s, 11725.11/s (0.000 avg, 0.000 min, 0.003 max)
Read  25000 keys: 1.76s, 11725.11/s (0.000 avg, 0.000 min, 0.005 max)


pylibmc: gevent-08
Write 25000 keys: 2.82s, 8871.63/s (0.000 avg, 0.000 min, 0.003 max)
Read  25000 keys: 2.00s, 8871.63/s (0.000 avg, 0.000 min, 0.001 max)


pylibmc: gevent-04
Write 25000 keys: 2.27s, 11009.34/s (0.000 avg, 0.000 min, 0.004 max)
Read  25000 keys: 1.90s, 11009.34/s (0.000 avg, 0.000 min, 0.007 max)


pylibmc: gevent-02
Write 25000 keys: 3.14s, 7962.19/s (0.000 avg, 0.000 min, 0.002 max)
Read  25000 keys: 2.40s, 7962.19/s (0.000 avg, 0.000 min, 0.002 max)


ultramemcache: sync
Write for 25000 keys: 1.17s, 21375.73/s (0.000 avg, 0.000 min, 0.002 max)
Read for 25000 keys: 1.16s, 21375.73/s (0.000 avg, 0.000 min, 0.002 max)


ultramemcache: gevent-16
Write 25000 keys: 0.99s, 25230.86/s (0.000 avg, 0.000 min, 0.002 max)
Read  25000 keys: 1.04s, 25230.86/s (0.000 avg, 0.000 min, 0.002 max)


ultramemcache: gevent-08
Write 25000 keys: 0.98s, 25427.85/s (0.000 avg, 0.000 min, 0.004 max)
Read  25000 keys: 1.05s, 25427.85/s (0.000 avg, 0.000 min, 0.002 max)


ultramemcache: gevent-04
Write 25000 keys: 1.00s, 25004.15/s (0.000 avg, 0.000 min, 0.001 max)
Read  25000 keys: 1.07s, 25004.15/s (0.000 avg, 0.000 min, 0.008 max)


ultramemcache: gevent-02
Write 25000 keys: 0.95s, 26322.44/s (0.000 avg, 0.000 min, 0.001 max)
Read  25000 keys: 1.02s, 26322.44/s (0.000 avg, 0.000 min, 0.007 max)


