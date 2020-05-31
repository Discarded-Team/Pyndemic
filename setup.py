from setuptools import find_packages, setup

setup(
    name='Pyndemic',
    version='0.1.0',
    author='Discarded Team',
    author_email='geroyparagvay@gmail.com',
    description='A future digital version of Pandemic board game',
    license='GNU',
    packages=['pyndemic', 'pyndemic.ui'],
    include_package_data=True,
    package_data={'pyndemic': ['settings.cfg']}
)
