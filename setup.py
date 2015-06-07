from setuptools import setup, find_packages

setup(
    name="SPACESHIP",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Antoan Angelov",
    author_email="antoan.angelov+spaceship@gmail.com",
    description="Python utility for chat and streaming files across machines in the same network",
    license="MIT",
    keywords="spaceship python terminal chat stream files same network",
    classifiers=[
        "Development Status :: 3 - Alpha",
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