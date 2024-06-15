from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.readlines()

with open("README.md") as f:
    read_me = f.read()

setup(
    name="vehicle-routing-challenge",
    version="0.0.0",
    description="My solution attempting to optimize cost given a set of simple routes.",
    long_description=read_me,
    long_description_content_type="text/markdown; charset=UTF-8",
    author="Teagan Glenn",
    author_email="that@teagantotally.rocks",
    url="https://www.github.com/teagan42/Vehicle-Routing-Challenge",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    license="MIT",
    keywords="Vehicle Routing, Traveling Salesman",
    # entry_points={
    #     "console_scripts": [
    #
    #     ],
    # },
)
