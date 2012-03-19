#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import sys
import ujson
import time
import pylibmc

pool_size = int(sys.argv[1])
pool = Pool(pool_size)

client = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True})
data = ujson.load(open("data.json"))

def timer(a):
    f, args, timings = a
    t0 = time.time()
    ret = f(*args)
    timings.append(time.time() - t0)
    return ret

values = set(data.values())

read_times = []
read_outcomes = []
write_times = []

def appender(expected, val, list):
    list.append(expected == val)

t0 = time.time()
pool.map(timer, [(client.set, (str(key), str(val)), write_times) for key,val in data.iteritems()])
t1 = time.time()
read_outcomes = pool.map(timer, [(client.get, (str(key),), read_times) for key,val in data.iteritems()])
t2 = time.time()

read_outcomes = [r in values for r in read_outcomes]

if not all(read_outcomes):
    print "ERROR: %d read errors" % read_outcomes.count(False)

n = len(data)
print "Write %d keys: %0.2fs, %0.2f/s (%0.3f avg, %0.3f min, %0.3f max)" % (
    n, t1-t0, n/(t1-t0), (t1-t0)/float(n), min(write_times), max(write_times)
)
print "Read  %d keys: %0.2fs, %0.2f/s (%0.3f avg, %0.3f min, %0.3f max)" % (
    n, t2-t1, n/(t1-t0), (t2-t1)/float(n), min(read_times), max(read_times)
)


