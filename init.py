#! /usr/bin/python
"""Tiny init tool.
"""

from __future__ import print_function

import argparse
import errno
import fcntl
import logging
import os
import os.path
import signal
import sys

import psutil

cli = argparse.ArgumentParser()
cli.add_argument('--debug', 
                 action='store_const', dest='loglevel', 
                 const=logging.DEBUG, default=logging.INFO, 
                 help="Enable debug output")
cli.add_argument('--lock-file', help="Acquire an exclusive file lock",
                 metavar="FILENAME")
cli.add_argument('--lock-content', help="Content to write into lock file",
                 metavar="CONTENT")
cli.add_argument('command')
cli.add_argument('args', nargs=argparse.REMAINDER)
args = cli.parse_args()

FORMAT = '%(asctime)-15s init %(levelname)s: %(message)s'
logging.basicConfig(level=args.loglevel, format=FORMAT)
logger = logging.getLogger()

logger.debug("command line args: %s", args)

selfp = psutil.Process()
logger.debug("my pid: %d", selfp.pid)


class AlreadyLockedError(OSError):
    pass

class filelock:
    """Acquire a lock on a file.

    Open a lock file and acquire a lock on it.  The file is created if
    it does not already exist.  The parent directory must be writable.
    Do nothing if the given file name evaluates to False.

    This may either be used as a context manager or by calling the
    constructor and the release() method explicitly.
    """
    def __init__(self, filename, content=None, mode=fcntl.LOCK_EX):
        if filename:
            logger.debug("trying to lock %s ...", filename)
            self.fd = os.open(filename, os.O_RDWR | os.O_CREAT)
            try:
                fcntl.lockf(self.fd, mode | fcntl.LOCK_NB)
            except Exception as e:
                self.release()
                if (isinstance(e, (OSError, IOError)) and 
                    e.errno in (errno.EACCES, errno.EAGAIN)):
                    e = AlreadyLockedError(*e.args)
                raise e
            logger.debug("lock on %s acquired.", filename)
            if content and mode == fcntl.LOCK_EX:
                os.ftruncate(self.fd, 0)
                os.write(self.fd, content.encode('utf8'))
        else:
            self.fd = None

    def release(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def __del__(self):
        self.release()


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


try:
    with filelock(args.lock_file, args.lock_content):

        # Launch the command indicated in the command line.
        command = [args.command] + args.args
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

except AlreadyLockedError:
    logger.critical("lockfile %s is already locked.", args.lock_file)
    sys.exit(1)
