from setuptools import setup, find_packages
import os

VERSION = "0.0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

# TODO: Setup Pypi repository
setup(
    name="docdb",
    description="Async Document Database Interface With ODM",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    #url="",
    version=VERSION,
    entry_points={
        'console_scripts': [
            'document_database=document_database.__init__:main',
        ]
    },
    packages=find_packages(),
    install_requires=[
        "pydantic==1.8.2"
    ],
    extras_require={
        "mongo": ["motor==2.5.1"],
        "test": ["tox==3.24.4"]
    },
    tests_require=[
        "docdb[test]"
    ],
    python_requires=">=3.8",
)
