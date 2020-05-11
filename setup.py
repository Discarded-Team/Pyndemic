from setuptools import find_packages, setup

setup(
    name="Pyndemic",
    version="0.1.0",
    packages=find_packages('src', exclude=['test']),
    author="Discarded Team",
    author_email="geroyparagvay@gmail.com",
    description="A future digital version of Pandemic board game",
    license='GNU',
)
