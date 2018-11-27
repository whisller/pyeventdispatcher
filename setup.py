import json
import os
from setuptools import setup, find_packages

from pyeventdispatcher import __version__

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")) as f:
    README = f.read()

with open("Pipfile.lock") as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data["version"]
        for package_name, package_data in lock_data["default"].items()
    ]
    tests_require = [
        package_name + package_data["version"]
        for package_name, package_data in lock_data["develop"].items()
    ]

setup(
    name="pyeventdispatcher",
    description="",
    version=__version__,
    long_description=README,
    install_requires=install_requires,
    tests_require=tests_require,
    packages=find_packages(),
    include_package_data=True
)
