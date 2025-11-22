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

Python:

+ Python 3.6 or newer.

Required library packages:

+ `setuptools`_

+ `psutil`_ >= 2.0

Optional library packages:

+ `git-props`_

  This package is used to extract some metadata such as the version
  number out of git, the version control system.  All releases embed
  that metadata in the distribution.  So this package is only needed
  to build out of the plain development source tree as cloned from
  GitHub, but not to build a release distribution.


Copyright and License
---------------------

Copyright 2016–2025 Rolf Krahl

Licensed under the `Apache License`_, Version 2.0 (the "License"); you
may not use this package except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _setuptools: https://github.com/pypa/setuptools/
.. _psutil: https://pypi.python.org/pypi/psutil/
.. _git-props: https://github.com/RKrahl/git-props
.. _Apache License: https://www.apache.org/licenses/LICENSE-2.0
