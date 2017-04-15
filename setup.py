"""contains instructions for setuptools"""

from setuptools import setup, find_packages

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="rrm",
    packages=find_packages(),
    entry_points={
        "console_scripts": ['rrm = rrm.terminal_rm.main:main']
    },
    long_description = long_descr,
    version='1.0',
    description="rm on steroids",
    author="Chachura Rodion",
    author_email="geekrodion@gmail.com",
    url="https://github.com/RodionChachura/rrm",
    install_requires=['python-crontab']
)