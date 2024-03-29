Caveats
=======

* **monitor** merely samples data made available by other libraries or command-line
  tools. In the case of CPU resources the **psutil** library in Python. In the case of
  GPU resources the output of the ``nvidia-smi`` tool. Metrics are reported with regard
  to the whole system, NOT JUST YOUR APPLICATION.

* For GPU resources, currently only ``nvidia-smi`` and ``rocm-smi`` are supported.
  Additional GPU providers could be supported in the future though.

* Sampling more frequently than 1 second is an error. The CPU percent utilization is
  a time averaged metric subject to how frequently it is sampled.


.. toctree::
    :maxdepth: 2
    :caption: Contents:
