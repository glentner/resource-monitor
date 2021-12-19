Getting Started
===============


Installation
------------

**monitor** is built on Python 3.7+ and can be installed using Pip

.. code-block:: none

    pip install resource-monitor

For use with GPUs you will need to have the associated command-line tools installed.
Currently, Nvidia (using ``nvidia-smi``) and AMD (using ``rocm-smi``) are supported.


Basic Usage
-----------

The usage statement for each resource type is outlined below. The ``--help`` flag is
provided at each level. ``monitor --help`` will show the device groups (i.e., cpu/gpu).
``monitor <device> --help`` will show available resources for that group.

For complete information including examples at the command-line, the manual page can be
accessed with ``man monitor``.


CPU Percent
^^^^^^^^^^^

.. code-block:: none 
    :emphasize-lines: 1-2

    usage: monitor cpu percent [-h] [--all-cores] [-s SECONDS] [--csv [--no-header]]
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
    :emphasize-lines: 1-2

    usage: monitor cpu memory [-h] [-s SECONDS] [--actual [--human-readable]] [--csv [--no-header]]
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
    :emphasize-lines: 1-2

    usage: monitor gpu percent [-h] [-s SECONDS] [--csv [--no-header]]
    Monitor GPU percent utilization.

    options:
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


GPU Memory
^^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-2

    usage: monitor gpu memory [-h] [-s SECONDS] [--csv [--no-header]]
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
    :emphasize-lines: 1-2

    usage: monitor gpu power [-h] [-s SECONDS] [--csv [--no-header]]
    Monitor GPU power consumption (in Watts).

    options:
    -s, --sample-rate  SECONDS     Time between samples (default: 1).
        --plain                    Print messages in syslog format (default).
        --csv                      Print messages in CSV format.
        --no-header                Suppress printing header in CSV mode.
    -h, --help                     Show this message and exit.


GPU Temperature 
^^^^^^^^^^^^^^^

.. code-block:: none
    :emphasize-lines: 1-2

    usage: monitor gpu temp [-h] [-s SECONDS] [--csv [--no-header]]
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
