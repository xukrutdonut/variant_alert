from setuptools import setup, find_packages

setup(
    name="variant_alert",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pysam==0.15.3",
        "click>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "variant-alert=variant_alert.cli:variant_alert",
        ],
    },
)