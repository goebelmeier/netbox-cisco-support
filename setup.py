import codecs
import os.path

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='netbox-cisco-support',
    version=get_version('netbox_cisco_support/version.py'),
    description='Implementing Cisco Support APIs into NetBox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/goebelmeier/netbox-cisco-support',
    project_urls={
        "Bug Tracker": "https://github.com/goebelmeier/netbox-cisco-support/issues",
    },
    author='Timo Reimann',
    author_email='timo@goebelmeier.de',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration"
    ],
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
