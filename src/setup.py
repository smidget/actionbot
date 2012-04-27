#!/usr/bin/env python

"""
setup.py file for SWIG robochair
"""

from distutils.core import setup, Extension


robochair_module = Extension('_robochair',
                           sources=['RoboteqDevice.cpp', 'robochair_wrap.cxx'],
                           )

setup (name = 'robochair',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig robochair from docs""",
       ext_modules = [robochair_module],
       py_modules = ["robochair"],
       )
