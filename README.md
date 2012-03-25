memcached/gevent benchmarks
----------------------------

Small repos with some testing scripts that attempt to benchmark the latency of
making memcached requests with various python libraries.  The key/value pairs in
data.json are all small strings (uuids), so this is not a test of throughput or
even perhaps real world performance if you are storing large objects.

method
------

libraries are tested standalone (in a serial method) and under gevent which
attempts to use a greenpool to parallelize 2, 4, 8, and 16 ways.  Running
`test.py` will run all tests and update this file with the results.

results
-------


### pylibmc set (25000 keys)

               elapsed      rate       avg        min        max    
    sync        1.410    17772.100    0.000      0.000      0.003   
    gevent-16   2.200    11369.710    0.000      0.000      0.004   
    gevent-08   2.860     8746.570    0.000      0.000      0.002   
    gevent-04   3.480     7189.510    0.000      0.000      0.005   
    gevent-02   3.060     8157.030    0.000      0.000      0.003   

### pylibmc get (25000 keys)

               elapsed      rate       avg        min        max    
    sync        1.310    17772.100    0.000      0.000      0.001   
    gevent-16   2.220    11369.710    0.000      0.000      0.003   
    gevent-08   2.470     8746.570    0.000      0.000      0.003   
    gevent-04   2.030     7189.510    0.000      0.000      0.002   
    gevent-02   2.620     8157.030    0.000      0.000      0.003   

### ultramemcache set (25000 keys)

               elapsed      rate       avg        min        max    
    sync        1.420    17573.050    0.000      0.000      0.003   
    gevent-16   0.980    25587.990    0.000      0.000      0.002   
    gevent-08   1.000    25033.070    0.000      0.000      0.010   
    gevent-04   0.990    25145.390    0.000      0.000      0.003   
    gevent-02   0.970    25808.930    0.000      0.000      0.002   

### ultramemcache get (25000 keys)

               elapsed      rate       avg        min        max    
    sync        1.220    17573.050    0.000      0.000      0.003   
    gevent-16   1.030    25587.990    0.000      0.000      0.002   
    gevent-08   1.050    25033.070    0.000      0.000      0.002   
    gevent-04   1.020    25145.390    0.000      0.000      0.002   
    gevent-02   1.010    25808.930    0.000      0.000      0.003   
