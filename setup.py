#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for variant_alert package.
This provides compatibility for pip install when poetry is not available.
"""

from setuptools import setup, find_packages

setup(
    name="variant_alert",
    version="0.1.0",
    description="Compare two clinvar VCF version and output differences of classification between gene and variants. Can also generate a clinvarome file.",
    author="Mélanie Broutin, Abdoulaye Diallo, Raphaël Lanos, Kévin Yauy",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "pysam>=0.15.3",
        "click>=7.0,<8.0",
        "flask>=2.0,<3.0",
        "werkzeug>=2.0,<3.0",
    ],
    extras_require={
        'web': [
            'flask>=2.0,<3.0',
            'werkzeug>=2.0,<3.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'variant-alert=variant_alert.cli:variant_alert',
            'variant-alert-web=web.app:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers", 
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)