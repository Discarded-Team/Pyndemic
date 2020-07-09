import re

from setuptools import find_packages, setup


with open('pyndemic/__init__.py') as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='Pyndemic',
    version=version,
    author='Discarded Team',
    author_email='geroyparagvay@gmail.com',
    description='A future digital version of Pandemic board game',
    license='GNU',
    packages=['pyndemic', 'pyndemic.core', 'pyndemic.ui'],
    include_package_data=True,
    package_data={'pyndemic': ['settings.cfg']}
)
