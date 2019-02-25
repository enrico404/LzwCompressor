#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='LzwCompressor',
      version='1.0',
      description='Lempel Ziv Welch compressor and decompressor',
      author='Sedoni Enrico',
      author_email='sedoni.enrico@gmail.com',
      license='MIT',
      packages=['LzwCompressor','LzwCompressor.utils'],
      scripts=['LzwCompressor/scripts/compress.py','LzwCompressor/scripts/uncompress.py']
     )
