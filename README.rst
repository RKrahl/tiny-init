A minimal implementation of an init process
===========================================

The init process is the parent of all other processes.  This package
provides a Python script as a rather minimal implementation.  It takes
a command as argument and spawns a sub process.  Then it waits for
child processes, propagates signals to them, and reaps those that are
terminated.  If the last child process is gone, it terminates itself.

Normally, the init process is provided by the operation system, in
packages like systemd or sysvinit.  The tiny-init package is useful in
environments that do not have a native init process, such as docker
containers.


System requirements
-------------------

+ Python 2.6, 2.7, or 3.1 and newer.

+ `psutil`_ >= 2.0


Installation
------------

This package uses the distutils Python standard library package and
follows its conventions of packaging source distributions.  See the
documentation on `Installing Python Modules`_ for details or to
customize the install process.  You typically want to install the init
script into a system binary directory, use `--install-scripts` to
override the default.

1. Download the sources, unpack, and change into the source
   directory.

2. Install::

     $ python setup.py install --install-scripts /usr/local/sbin


Copyright and License
---------------------

Copyright 2016
Helmholtz-Zentrum Berlin für Materialien und Energie GmbH

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _psutil: https://pypi.python.org/pypi/psutil/
.. _Installing Python Modules: https://docs.python.org/2.7/install/
