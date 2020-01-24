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
from setuptools import setup, find_packages

# metadata
from monitor.__meta__ import (__version__, __authors__,
                              __contact__, __license__, __description__,
                              __keywords__, __website__)


with open('README.rst', mode='r') as readme:
    long_description = readme.read()


setup(
    name                 = 'resource-monitor',
    version              = __version__,
    author               = __authors__,
    author_email         = __contact__,
    description          = __description__,
    license              = __license__,
    keywords             = __keywords__,
    url                  = __website__,
    packages             = find_packages(),
    long_description     = long_description,
    classifiers          = ['Development Status :: 4 - Beta',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Operating System :: POSIX :: Linux',
                            'Operating System :: MacOS',
                            'Intended Audience :: Information Technology',
                            'Intended Audience :: System Administrators',
                            'License :: OSI Approved :: Apache Software License',
                            'Topic :: System :: Monitoring',
                            ],
    entry_points         = {'console_scripts': ['monitor=monitor.cli:main']},
    install_requires     = ['cmdkit>=1.2.1', 'logalpha>=2.0.2', 'psutil'],
    extras_require       = {
        'dev': ['ipython', 'pytest', 'hypothesis', 'pylint', 'sphinx',
                'sphinx-rtd-theme']},
)
