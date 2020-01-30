Manual Page for Monitor 
=======================

Synopsis
--------

monitor *device* *resource* [--sample-rate *SECONDS*] [--csv [--no-header]]


Description
-----------

The ``monitor`` utility collects telemetry on system resources. Metrics are printed to
*stdout* at regular intervals. Resources are organized under "cpu" or "gpu" *device*
groups. All resources share some ``global options``, see below. The following list the
possible invocations and associated specific options.

    monitor cpu percent [--help]
        Collect telemetry on CPU core utilization.

        --total
            Report metrics as a total across all cores (default).

        --all-cores
            Report metrics on a per-core basis.

    monitor cpu memory [--help]
        Collect telemetry on CPU memory utilization.

        --percent
            Report metrics as a percent of total available memory (default).

        --actual
            Report metrics as actual memory allocated (in bytes).

        -H, --human-readable
            Report metrics in a human readable format with units (e.g., "8.2G").

    monitor gpu percent [--help]
        Collect telemetry on GPU percent utilization.
    
    monitor gpu memory [--help]
        Collect telemetry on GPU percent memory utilization.
    
    monitor gpu power [--help]
        Collect telemetry on GPU percent power consumption.
    
    monitor gpu temp [--help]
        Collect telemetry on GPU temperature (Celsius).


Global Options
--------------

-s, --sample-rate *SECONDS*
    The time interval between consecutive samples (default: 1 second).

--plain
    Print messages in log format (default).

--csv
    Print messages in CSV format. The header is automatically included in the first line
    of output. The field names are consistent between resource types with the exception
    of the last one or two fields. For the ``--all-cores`` option with "cpu" and any
    of the "gpu" resources, a ``cpu_id`` or ``gpu_id`` is included. The last column is
    specific to the resource being monitored. See also: ``--no-header``.

--no-header
    Suppress printing the header in CSV mode (see ``--csv``). This is useful when
    appending data to a single file from one or more sources. See the distributed
    computing examples below.

-h, --help           
    Show help message and exit.

-v, --version        
    Show the version number and exit.


Examples
--------

Monitor CPU on a per-core basis on a 10 second interval.

.. code-block:: none

    $ monitor cpu percent --all-cores --sample-rate 10

    2020-01-30 12:55:55.521 some-hostname.local monitor.cpu.percent [0] 7.5
    2020-01-30 12:55:55.522 some-hostname.local monitor.cpu.percent [1] 2.3
    2020-01-30 12:55:55.522 some-hostname.local monitor.cpu.percent [2] 8.5
    2020-01-30 12:55:55.522 some-hostname.local monitor.cpu.percent [3] 0.8
    2020-01-30 12:56:05.525 some-hostname.local monitor.cpu.percent [0] 8.5
    2020-01-30 12:56:05.525 some-hostname.local monitor.cpu.percent [1] 2.3
    2020-01-30 12:56:05.525 some-hostname.local monitor.cpu.percent [2] 8.6
    2020-01-30 12:56:05.526 some-hostname.local monitor.cpu.percent [3] 0.8
    ...

Monitor CPU memory in actual bytes used and output in CSV format.

.. code-block:: none

    $ monitor cpu memory --actual --csv

    timestamp,hostname,resource,memory_used
    2020-01-30 12:58:21.476,some-hostname.local,cpu.memory,9707892736
    2020-01-30 12:58:22.479,some-hostname.local,cpu.memory,9706946560
    2020-01-30 12:58:23.480,some-hostname.local,cpu.memory,9724190720
    2020-01-30 12:58:24.484,some-hostname.local,cpu.memory,9726636032
    ...

Monitor GPU utilization on a per-GPU basis on a 10 second interval and log to a file.

.. code-block:: none

    $ monitor gpu percent --sample-rate 10 >gpu.memory.log
    $ head -8 gpu.memory.log

    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [0] 79.0
    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [1] 0.0
    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [2] 0.0
    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [3] 87.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [0] 72.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [1] 0.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [2] 0.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [3] 90.0

Monitor core utilization within a distributed computing context.

.. code-block:: none

    $ mpiexec -machinefile <(sort -u $NODEFILE) \
          monitor cpu percent --all-cores

    2020-01-30 13:17:50.980 node-001.cluster monitor.cpu.percent [0] 100.0
    2020-01-30 13:17:50.980 node-001.cluster monitor.cpu.percent [1] 1.0
    ...
    2020-01-30 13:17:51.208 node-002.cluster monitor.cpu.percent [0] 100.0
    2020-01-30 13:17:51.208 node-002.cluster monitor.cpu.percent [1] 100.0
    ...
    2020-01-30 13:17:51.294 node-003.cluster monitor.cpu.percent [0] 100.0
    2020-01-30 13:17:51.295 node-003.cluster monitor.cpu.percent [1] 100.0
    ...
    2020-01-30 13:17:51.319 node-004.cluster monitor.cpu.percent [0] 100.0
    2020-01-30 13:17:51.320 node-004.cluster monitor.cpu.percent [1] 100.0
    ...

Monitor percent main memory utilization within a distributed computing context, as a
background task, and in CSV format. Basically, the produced headers will arrive from each
node, suppress them with ``--no-header``. Create a single header by just slicing it off
the top of an initial invocation. Collect the process ID so the task can be interrupted
at then end of your job.

.. code-block:: none

    $ monitor cpu memory --csv | head -1 >log/resource.mem.csv
    $ mpiexec -machinefile <(sort -u $NODEFILE) \
          monitor cpu memory --csv --no-header >>log/resource.mem.csv &
    $ MEM_PID=$!

    ...

    $ kill -s INT $MEM_PID


Recommendations
---------------

* If collecting data for benchmarking/profiling/scaling purposes (regarding CPU/memory in particular),
  it may be appropriate to also collect data in the absense of your application as a null-scenario.
  This can approximate a "background noise" that can modeled and subtracted.


Caveats
-------

* ``monitor`` merely samples data made available by other libraries or command line
  tools. In the case of CPU resources the ``psutil`` library in Python. In the case of
  GPU resources the output of the ``nvidia-smi`` tool. Metrics are reported with regard
  to the whole system, NOT JUST YOUR APPLICATION.

* For GPU resources, currently only NVIDIA GPUs are supported per ``nvidia-smi``.
  However, code has been included that makes it trivial to support additional resources
  that report via some command line invocation (i.e., some other GPU provider).

* Sampling more frequently than 1 second is an error. The CPU percent utilization is
  a time averaged metric subject to how frequently it is sampled.


See Also
--------

nvidia-smi(1), head(1), mpiexec(1), sort(1)
