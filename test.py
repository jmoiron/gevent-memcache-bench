#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test memcached performance."""

from subprocess import Popen, PIPE, STDOUT
from pprint import pprint

import pylibmc
import umemcache

def run(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    p.wait()
    return p.stdout.read()

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

for key in sorted(results):
    for run in sorted(results[key], reverse=True):
        wreadme.write("%s: %s\n" % (key, run))
        wreadme.write(results[key][run])
        wreadme.write("\n\n")

wreadme.close()

