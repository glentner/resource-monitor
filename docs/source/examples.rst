Examples
========


Simple
------

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

    $ monitor gpu percent --sample-rate 10 >gpu.percent.log
    $ head -8 gpu.percent.log

    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [0] 79.0
    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [1] 0.0
    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [2] 0.0
    2020-01-30 13:04:22.938 node-001.cluster monitor.gpu.percent [3] 87.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [0] 72.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [1] 0.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [2] 0.0
    2020-01-30 13:04:33.196 node-001.cluster monitor.gpu.percent [3] 90.0


Distributed
-----------

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


.. toctree::
    :maxdepth: 2
    :caption: Contents:
