#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ujson
import time
import umemcache

client = umemcache.Client("127.0.0.1:11211")
client.connect()
data = ujson.load(open("data.json"))

def timer(f, args, timings):
    t0 = time.time()
    ret = f(*args)
    timings.append(time.time() - t0)
    return ret

read_times = []
read_outcomes = []
write_times = []

t0 = time.time()
for key,val in data.iteritems():
    timer(client.set, (str(key), str(val)), write_times)
t1 = time.time()
for key,val in data.iteritems():
    read_outcomes.append(val == timer(client.get, (str(key),), read_times)[0])
t2 = time.time()

if not all(read_outcomes):
    print "# ERROR: %d read errors" % read_outcomes.count(False)

n = len(data)
print "# num elapsed rate avg min max"
print "%d %0.2f %0.2f %0.3f %0.3f %0.3f" % (
    n, t1-t0, n/(t1-t0), (t1-t0)/float(n), min(write_times), max(write_times)
)
print "%d %0.2f %0.2f %0.3f %0.3f %0.3f" % (
    n, t2-t1, n/(t1-t0), (t2-t1)/float(n), min(read_times), max(read_times)
)

