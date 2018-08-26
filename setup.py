from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='almanak',
    version='0.1.3',
    author='Claus Juhl Knudsen',
    author_email='clausjuhl@yahoo.com',
    packages=find_packages(),
    description='Almanak-module.',
    long_description=long_description,
    url='https://github.com/clausjuhl/almanak',
    include_package_data=True,
    license='MIT',
    python_requires='>=3.6.2',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)