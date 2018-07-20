#! /usr/bin/python

from distutils.core import setup

setup(
    name = "tiny-init",
    version = "0.4",
    description = "A minimal implementation of an init process",
    author = "Rolf Krahl",
    author_email = "rolf.krahl@helmholtz-berlin.de",
    url = "https://github.com/RKrahl/tiny-init",
    license = "Apache-2.0",
    requires = ["psutil"],
    scripts = ["init.py"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Topic :: System :: Boot :: Init",
        ],
)

