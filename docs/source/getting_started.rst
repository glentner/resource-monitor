Getting Started
===============


Installation
------------

**monitor** is built on Python 3.7+ and can be installed using Pip

.. code-block:: none

    pip install resource-monitor

For use with GPUs you will need to have the associated command line tools installed.
Currently, only NVIDIA is implemented (using ``nvidia-smi``).


Basic Usage
-----------

The usage statement for each resource type is outlines below. The ``--help`` flag is
provided at each level. ``monitor --help`` will show the device groups (i.e., cpu/gpu).
``monitor <device> --help`` will show available resources for that group.

For complete information including examples at the command line, the manual page can be
accessed with ``man monitor``.


CPU Percent
^^^^^^^^^^^

.. code-block:: none 
    :emphasize-lines: 1-3

    usage: monitor cpu percent [--total | --all-cores] [--sample-rate SECONDS]
                               [--plain | --csv [--no-header]]
                               [--help]

    Monitor CPU percent utilization.

    options:
    -t, --total                    Show values for total cpu usage (default).
    -a, --all-cores                Show values for individual cores.
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


CPU Memory
^^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-3

    usage: monitor cpu memory [--percent | --actual] [--sample-rate SECONDS] [--human-readable]
                              [--plain | --csv [--no-header]]
                              [--help]

    Monitor CPU memory utilization.

    options:
        --percent                   Report value as a percentage (default).
        --actual                    Report value as total bytes.
    -s, --sample-rate     SECONDS   Time between samples (default: 1).
    -H, --human-readable            Human readable values (e.g., "8.2G").
        --plain                     Print messages in syslog format (default).
        --csv                       Print messages in CSV format.
        --no-header                 Suppress printing header in CSV mode.
    -h, --help                      Show this message and exit.


GPU Percent
^^^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-3

    usage: monitor gpu percent [--sample-rate SECONDS]
                               [--plain | --csv [--no-header]]
                               [--help]

    Monitor GPU volatile utilization.

    options:
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


GPU Memory
^^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-3

    usage: monitor gpu memory [--sample-rate SECONDS]
                              [--plain | --csv [--no-header]]
                              [--help]

    Monitor GPU memory utilization.

    options:
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


GPU Power
^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-3

    usage: monitor gpu power [--sample-rate SECONDS]
                             [--plain | --csv [--no-header]]
                             [--help]

    Monitor GPU power consumption (percent maximum).

    options:
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


GPU Temperature 
^^^^^^^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-3

    usage: monitor gpu temp [--sample-rate SECONDS]
                            [--plain | --csv [--no-header]]
                            [--help]

    Monitor GPU temperature (Celsius).

    options:
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


.. toctree::
    :maxdepth: 2
    :caption: Contents:
