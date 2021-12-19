For Developers
==============


Roadmap
-------

* Explore additional resources (e.g., disk/filesystem, threads).


Contributing
------------

Development of **monitor** happens on `Github <https://github.com/glentner/monitor>`_.
Contributions are welcome in the form of suggestions for additional features, *Pull
Requests* with new features or bug fixes, etc. If you find bugs or have questions, open
an *Issue*.


Guide
-----

The **monitor** command-line interface is written in Python and uses the **psutil**
library. Additional resources may be possible to collect but may not necessarily be
easily made cross-platform.

The GPU functionality is simply a wrapper external tools, e.g., ``nvidia-smi``.
In the library, a fully generalized notion of an *ExternalMetric* interface is provided.
In principle, anything that could conceivably be invoked on the
command-line need only have a parser method implemented.

For example:

.. code-block:: python

    class OpenFiles(ExternalMetric):
        """Report the number of open files (psutil already provides this)."""

        _cmd = 'lsof -u `whoami`'

        @classmethod
        def parse_text(cls, block: str) -> Dict[str, int]:
            """Count lines in the output."""
            return {'count': len(block.strip().split('\n'))}


.. toctree::
    :maxdepth: 2
    :caption: Contents:
