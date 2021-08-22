Introduction
============

What
************

``macrame`` is a utility to help the developer when building, testing, debugging and interacting with hardware and software on ``Assembly/C/C++ embedded projects``.
It is based on ``GNU Make`` but it is not another build system.
It provides a Make abstraction for an easy and intuitive way to interact commonly with development processes on different projects by hiding complexities from the developer.
In essence, this package is not a replacement of Make and Makefiles but rather an customized abstraction.

Why
**********

During the developing of embedded systems one has to interact with various boards, microcontrollers and tools.
If not hiding behind an IDE and using a real build system like GNU Make then the developer finds himself copying his Makefile over and over between his projects and adapting it.
At some point the Makefile changes are lost. A feature of ``macrame`` is to solve this.

How
**********

The current implementation has been developed in Python 3 and tested on Linux.
