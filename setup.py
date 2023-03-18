import os

from setuptools import setup

from kenbundata import (
    __author__,
    __description__,
    __email__,
    __package_name__,
    __version__,
)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"), "r") as fin:
    __long_description__ = fin.read()

setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    license="MIT",
    url="https://github.com/kenbun-app/kenbun-data",
    description=__description__,
    long_description=__long_description__,
    long_description_content_type="text/markdown",
    package_data={__package_name__: ["py.typed"]},
    packages=[__package_name__],
    install_requires=["pydantic", "pyhumps", "pillow"],
    extras_require={
        "dev": [
            "flake8",
            "pytest",
            "black",
            "mypy",
            "tox",
            "isort",
            "pytest-mock",
            "pytest-cov",
            "freezegun",
            "types-Pillow",
        ],
    },
)
