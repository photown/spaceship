from setuptools import setup, find_packages

setup(
    name="spaceship",
    version="0.7",
    packages=find_packages(),
    install_requires=[
        'netifaces'
    ],
    url = 'https://github.com/antoan-angelov/spaceship/',
    author="Antoan Angelov",
    author_email="antoan.angelov+spaceship@gmail.com",
    description="Python utility for chat and streaming files across machines in the same network",
    license="MIT",
    keywords="spaceship python terminal chat stream files same network",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.4",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    entry_points={
          'console_scripts': [
              'spaceship = spaceship.__main__:main'
          ]
      }
)