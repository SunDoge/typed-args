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


def read_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()

    return long_description


VERSION = find_version('typed_args', '__init__.py')

requirements = [
]

setup(
    name='typed-args',
    version=VERSION,
    author='SunDoge',
    author_email='384813529@qq.com',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/SunDoge/typedargs',
    packages=find_packages(exclude=['test']),
    install_requires=requirements,
)
