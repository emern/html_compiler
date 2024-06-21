from setuptools import setup, find_packages

setup(
    name='html_compiler',
    version='1.0',
    install_requires=[
        'markdown',
        'pyyaml'
    ],
    packages=find_packages(),
    author="Emery Nagy"
)
