"""Setup.py for Template project."""
from setuptools import setup, find_packages

# List of requirements
requirements = []  # This could be retrieved from requirements.txt

# Package (minimal) configuration
setup(
    name="Template",
    version="0.1.0",
    description="A template project",
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements,
    include_package_data=True,
)
