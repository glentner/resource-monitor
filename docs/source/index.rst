.. Resource Monitor documentation master file, created by
   sphinx-quickstart on Thu Jan 23 23:14:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Resource Monitor 
================

*A simple cross-platform system resource monitor.*


The **monitor** utility collects telemetry on system resources. Metrics are printed to
*stdout* at regular intervals. Resources are organized under "cpu" or "gpu" *device*
groups. All resources share some global options. 

It is easily installable, has an intuitive interface, and is cross-platform. Python 3.7
or higher is required, however.

.. code-block:: none
    
    pip install resource-monitor

.. code-block:: none

    $ monitor
    usage: monitor <device> <resource> [<args>...]
                   [--help] [--version]

    A simple cross-platform system resource monitor.

.. code-block:: none

    $ monitor cpu memory --actual --human-readable
    2020-01-30 15:24:51.573 desktop.local monitor.cpu.memory 8.23G
    2020-01-30 15:24:52.578 desktop.local monitor.cpu.memory 8.23G
    ...

.. toctree::
    :maxdepth: 2
    :caption: Contents:
    :hidden:

    getting_started
    examples
    recommendations
    caveats
    developers
