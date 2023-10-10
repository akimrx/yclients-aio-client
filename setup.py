#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup, find_packages

cwd = path.abspath(path.dirname(__file__))


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    return long_description


def metadata():
    meta = {}
    with open(path.join(cwd, "yclients_aio_client", "__version__.py"), "r") as fh:
        exec(fh.read(), meta)  # nosec

    return meta


def requirements():
    requirements_list = []

    with open("requirements.txt") as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


metadata = metadata()
readme = readme()
packages = find_packages()
requirements = requirements()


setup(
    name="yclients-aio-client",
    version="{{PKG_VERSION}}",
    author=metadata.get("author"),
    author_email=metadata.get("author_email"),
    license=metadata.get("license"),
    description=metadata.get("description"),
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms=metadata.get("platforms"),
    url=metadata.get("url"),
    keywords=metadata.get("keywords"),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=packages,
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.10",
    zip_safe=False,
)
