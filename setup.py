#!/usr/bin/env python3

from os import path, environ
from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    return long_description

cwd = path.abspath(path.dirname(__file__))


def metadata():
    meta = {}
    with open(path.join(cwd, "src", "__init__.py"), "r") as fh:
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

if environ.get("PYPI_FROM_GITHUB", 0) == 1:
    version = "{{PKG_VERSION}}"
else:
    version =  metadata.get("__version__")


def main():
    setup(
        name="gitlab-dumper",
        version=version,
        author=metadata.get("author"),
        author_email=metadata.get("author_email"),
        license=metadata.get("license"),
        description=metadata.get("description"),
        long_description=readme,
        long_description_content_type="text/markdown",
        url=metadata.get("url"),
        keywords=["gitlab"],
        platforms=["osx", "linux"],
        packages=packages,
        classifiers = [
            "Programming Language :: Python :: 3.10",
        ],
        install_requires=requirements,
        include_package_data=True,
        python_requires=">=3.10",
        entry_points={
            "console_scripts": [
                "gitlab-dumper=src.main:main"
            ]
        },
        zip_safe=False
    )


if __name__ == "__main__":
    main()
