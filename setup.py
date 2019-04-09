#!/usr/bin/python

import sys
import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()

# Specify the names of the pip packages which are required for this package to work
install_requires = [
    "pyyaml",
    "ansible",
    "yamlordereddictloader",
    "AnsibleModulePatcher",
    "ForemanApiWrapper"
]


if sys.version_info < (3, 0):
    install_requires.append("future")


# Specify the relative directory where the source code is being stored
# This is the root directory for the namespaces, packages, modules, etc.
source_code_dir = "src"


# Specify the name of the package as we want it to appear using pip
package_name = "AnsibleForemanModule"


setuptools.setup(
    name=package_name,
    version="1.0.0",
    author="tschneider",
    author_email="tschneider@live.com",
    description="An ansible module for utilizing the Foreman API v2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(source_code_dir),
    package_dir={
        "": source_code_dir
    },
    install_requires= install_requires,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
