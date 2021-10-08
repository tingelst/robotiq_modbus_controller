#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="robotiq_modbus_controller",
    version="0.0.0",
    description="A library for controlling Robotiq grippers over Modbus RTU and Modbus TCP",
    author="Lars Tingelstad",
    author_email="lars.tingelstad@ntnu.no",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pymodbus"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.6",
)
