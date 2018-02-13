# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools
import os

setuptools.setup(
    name="nionswift-hyperspy",
    version="0.0.1",
    author="Nion Software",
    author_email="swift@nion.com",
    description="Library and UI for using HyperSpy with Nion Swift.",
    long_description=open("README.rst").read(),
    url="https://github.com/nion-software/nionswift-hyperspy",
    packages=["nion.hyperspy", "nionswift_plugin.nion_hyperspy"],
    install_requires=['hyperspy'],
    license='GPLv3',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
    ],
    include_package_data=True,
    # This prevents package from being installed in zipped form. Otherwise it will not be recognized by Swift.
    # For more info see: https://setuptools.readthedocs.io/en/latest/setuptools.html#setting-the-zip-safe-flag
    zip_safe=False,
    test_suite="nion.hyperspy.test",
    python_requires='~=3.5',
)
