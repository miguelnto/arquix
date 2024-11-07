from setuptools import find_packages, setup

setup(
    name='arquix',
    packages=find_packages(include=['arquix', 'arquix.utils']),
    version='0.1.0',
    description='Workflow configuration manager for Arch-based distros.',
    author='Miguel Neto',
)
