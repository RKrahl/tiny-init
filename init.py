#! /usr/bin/python
"""Tiny init tool.
"""

from __future__ import print_function
import sys
import os
import errno
import signal
import logging
import psutil

if len(sys.argv) < 2:
    print("usage: %s cmd [args]" % sys.argv[0])
    sys.exit(1)

FORMAT = '%(asctime)-15s init %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger()

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

logger.debug("cmd: %s", " ".join(sys.argv[1:]))
pid = os.spawnvp(os.P_NOWAIT, sys.argv[1], sys.argv[1:])
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
