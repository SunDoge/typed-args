import io
import os
import re

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


VERSION = find_version('flame', '__init__.py')

requirements = [

]

setup(
    name='typeargs',
    version=VERSION,
    author='SunDoge',
    packages=find_packages(exclude=['test']),
    install_requires=requirements,
)
