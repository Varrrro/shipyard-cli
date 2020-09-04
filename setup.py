from setuptools import setup, find_packages

setup(
    name='shipyard-cli',
    version='0.1.0',
    author='Víctor Vázquez',
    author_email='victorvazrod@gmail.com',
    packages=find_packages(),
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
    python_requires='>=3.8'
)
