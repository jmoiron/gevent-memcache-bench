#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import sys
from itertools import chain
import ujson
import time
import umemcache

pool_size = int(sys.argv[1])
pool = Pool(pool_size)

client = umemcache.Client("127.0.0.1:11211")
client.connect()
data = ujson.load(open("data.json"))

def timer(f, args, timings):
    t0 = time.time()
    ret = f(*args)
    timings.append(time.time() - t0)
    return ret

values = set(data.values())
items = data.items()

def set_kvs(kvs):
    c = umemcache.Client("127.0.0.1:11211")
    c.connect()
    write_times = []
    for k,v in kvs:
        timer(c.set, (k, v), write_times)
    c.disconnect()
    return write_times

def get_kvs(kvs):
    c = umemcache.Client("127.0.0.1:11211")
    c.connect()
    read_times = []
    read_outcomes = [v == timer(c.get, (str(k),), read_times)[0] for k,v in kvs]
    c.disconnect()
    return read_times, read_outcomes

def piecegen(n, list):
    from math import ceil
    i=0
    l = len(list)
    s = int(ceil(l/float(n)))
    while i < l:
        yield list[i:i+s]
        i += s

chunks = list(piecegen(pool_size, items))

t0 = time.time()
write_times = pool.map(set_kvs, chunks)
t1 = time.time()
read_ret = pool.map(get_kvs, chunks)
t2 = time.time()

write_times = list(chain(*write_times))
read_outcomes = list(chain(*[r[1] for r in read_ret]))
read_times = list(chain(*[r[0] for r in read_ret]))

if not all(read_outcomes):
    print "ERROR: %d read errors" % read_outcomes.count(False)

n = len(data)
print "Write %d keys: %0.2fs, %0.2f/s (%0.3f avg, %0.3f min, %0.3f max)" % (
    n, t1-t0, n/(t1-t0), (t1-t0)/float(n), min(write_times), max(write_times)
)
print "Read  %d keys: %0.2fs, %0.2f/s (%0.3f avg, %0.3f min, %0.3f max)" % (
    n, t2-t1, n/(t1-t0), (t2-t1)/float(n), min(read_times), max(read_times)
)

