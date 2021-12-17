# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Setup and installation script for resource-monitor."""


# standard libs
import re
from setuptools import setup, find_packages


# load description from file
with open('README.rst', mode='r') as readme:
    long_description = readme.read()


# load metadata by parsing __init__ module
with open('monitor/__init__.py', mode='r') as source:
    content = source.read().strip()
    metadata = {key: re.search(key + r'\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)
                for key in ['__version__', '__authors__', '__contact__', '__license__',
                            '__website__', '__description__', '__keywords__', ]}

setup(
    name                 = 'resource-monitor',
    version              = metadata['__version__'],
    author               = metadata['__authors__'],
    author_email         = metadata['__contact__'],
    description          = metadata['__description__'],
    license              = metadata['__license__'],
    keywords             = metadata['__keywords__'],
    url                  = metadata['__website__'],
    packages             = find_packages(),
    long_description     = long_description,
    classifiers          = ['Development Status :: 5 - Production/Stable',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Programming Language :: Python :: 3.9',
                            'Programming Language :: Python :: 3.10',
                            'Operating System :: POSIX :: Linux',
                            'Operating System :: MacOS',
                            'Operating System :: Microsoft :: Windows',
                            'Intended Audience :: Information Technology',
                            'Intended Audience :: System Administrators',
                            'License :: OSI Approved :: Apache Software License',
                            'Topic :: System :: Monitoring',
                            ],
    entry_points         = {'console_scripts': ['monitor=monitor.cli:main']},
    install_requires     = ['cmdkit==1.5.5', 'logalpha==2.0.2', 'psutil>=5.7.2'],
    data_files = [
        ('share/man/man1', ['man/man1/monitor.1', ]),
    ],
)
