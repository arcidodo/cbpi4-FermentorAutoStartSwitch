from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cbpi4-FermentorAutoStartSwitch",
    version="0.0.1",
    description="CraftBeerPi4 Fermenter AutoStart Switch Plugin",
    author="Arco Veenhuizen",
    author_email="",
    url="https://github.com/arcidodo/cbpi4-FermentorAutoStartSwitch",
    license="GPLv3",
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst", "*.yaml"],
        "cbpi4-FermentorAutoStartSwitch": ["*", "*.txt", "*.rst", "*.yaml"],
    },
    packages=["cbpi4-FermentorAutoStartSwitch"],
    install_requires=[
        "cbpi4>=4.0.0.34",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
