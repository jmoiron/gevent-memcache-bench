#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test memcached performance."""

import sys
from collections import namedtuple
from subprocess import Popen, PIPE, STDOUT
from pprint import pprint

import pylibmc
import umemcache

keys = 'num elapsed rate avg min max'
Result = namedtuple('Result', keys)
keys = keys.split()

def run(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    p.wait()
    text = filter(None, p.stdout.read().split('\n'))
    for line in text:
        if 'ERROR' in line:
            raise Exception(line)
    text = [l for l in text if not l.startswith('#')]
    write, read = map(str.strip, text)
    write = map(float, write.split())
    read = map(float, read.split())
    return Result(*write), Result(*read)

versions = {
    'pylibmc': pylibmc.__version__,
    'ultramemcache': 'git'
}

results = {k:{} for k in sorted(versions)}

for key in versions:
    results[key]['sync'] = run(['./test-%s.py' % key])
    results[key]['gevent-02'] = run(['./test-%s-gevent.py' % (key), '2'])
    results[key]['gevent-04'] = run(['./test-%s-gevent.py' % (key), '4'])
    results[key]['gevent-08'] = run(['./test-%s-gevent.py' % (key), '8'])
    results[key]['gevent-16'] = run(['./test-%s-gevent.py' % (key), '16'])

readme = open('README.md').read()
results_line = 'results\n-------\n'
header = readme.split(results_line)[0]

wreadme = open('README.md', 'w')
wreadme.write(header + results_line + '\n')

for lib in sorted(versions):
    wreadme.write("\n### %s set (%d keys)\n\n" % (lib, results[lib]['sync'][0].num))

    wreadme.write("    " + " "*10 + ("%s %s %s %s %s\n" % tuple([k.center(10) for k in keys[1:]])))
    for run in sorted(results[lib], reverse=True):
        vals = results[lib][run][0]
        wreadme.write("    " + run.ljust(10) + ("%s %s %s %s %s\n" % tuple([('%0.3f' % getattr(vals, k)).center(10) for k in keys[1:]])))
    
    wreadme.write("\n### %s get (%d keys)\n\n" % (lib, results[lib]['sync'][0].num))

    wreadme.write("    " + " "*10 + ("%s %s %s %s %s\n" % tuple([k.center(10) for k in keys[1:]])))
    for run in sorted(results[lib], reverse=True):
        vals = results[lib][run][1]
        wreadme.write("    " + run.ljust(10) + ("%s %s %s %s %s\n" % tuple([('%0.3f' % getattr(vals, k)).center(10) for k in keys[1:]])))

wreadme.close()

