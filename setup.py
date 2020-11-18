import pathlib

from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='shipyard-cli',
    version='0.1.0',
    description='Command-line client for the Shipyard system',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/varrrro/shipyard-cli',
    author='Víctor Vázquez',
    author_email='victorvazrod@ugr.es',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=[
        'click',
        'marshmallow',
        'marshmallow_dataclass',
        'requests',
        'bson'
    ],
    entry_points='''
        [console_scripts]
        shipyard=shipyard_cli.main:cli
    ''',
    python_requires='>=3.6'
)
