#! /usr/bin/python
"""Tiny init tool.
"""

from __future__ import print_function

import argparse
import errno
import logging
import os
import signal
import sys

import psutil

cli = argparse.ArgumentParser()
cli.add_argument('--debug', 
                 action='store_const', dest='loglevel', 
                 const=logging.DEBUG, default=logging.INFO, 
                 help="Enable debug output")
cli.add_argument('command')
cli.add_argument('args', nargs=argparse.REMAINDER)
args = cli.parse_args()

FORMAT = '%(asctime)-15s init %(levelname)s: %(message)s'
logging.basicConfig(level=args.loglevel, format=FORMAT)
logger = logging.getLogger()

logger.debug("command line args: %s", args)

selfp = psutil.Process()
logger.debug("my pid: %d", selfp.pid)


# Propagate SIGHUP and SIGINT to direct children and SIGTERM to all
# descendants.

def sendtoall(signum, frame):
    for ch in selfp.children(recursive=True):
        os.kill(ch.pid, signum)

def sendtochilds(signum, frame):
    for ch in selfp.children(recursive=False):
        os.kill(ch.pid, signum)

signal.signal(signal.SIGTERM, sendtoall)
signal.signal(signal.SIGHUP, sendtochilds)
signal.signal(signal.SIGINT, sendtochilds)


# Launch the command indicated in the command line.

command = [args.command, *args.args]
logger.debug("cmd: %s", " ".join(command))
pid = os.spawnvp(os.P_NOWAIT, args.command, command)
logger.debug("cmd pid: %d", pid)


# Wait for all children to terminate, reaping zombies.

while True:
    try:
        (pid, status) = os.wait()
        logger.debug("reaped child %d with status %d", pid, status)
    except OSError as e:
        # Ignore EINTR, raise all other errors.
        if e.errno != errno.EINTR:
            raise
    if not selfp.children():
        logger.debug("last child is gone, terminating")
        break
