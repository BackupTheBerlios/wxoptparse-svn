# A setup script showing advanced features.
#
# Run with parameter: py2exe

from distutils.core import setup
import py2exe
import sys

setup(
    version = "0.1.1",
    name = "mytest",

    # targets to build
    console=["mytest.py"],
)

