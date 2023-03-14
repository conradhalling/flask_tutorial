"""
Describe the project and the files that belong to it.

This requires an additional file, MANIFEST.in.
"""

import setuptools

setuptools.setup(
    name="flaskr",
    version="1.0.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
    ],
)
