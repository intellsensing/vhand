# License: GPLv3

from os.path import realpath, dirname, join
from setuptools import setup, find_packages
import vhand

VERSION = vhand.__version__
PROJECT_ROOT = dirname(realpath(__file__))

setup(name = "vhand",
      version=VERSION,
      description = "Virtual hand interface in Python.",
      author = "Agamemnon Krasoulis",
      author_email = "agamemnon.krasoulis@gmail.com",
      url = "https://github.com/intellsensing/virtual_hand",
      packages=find_packages(),
      package_data={'': ['LICENSE.txt',
                         'README.md']
                    },
      include_package_data=True,
      license='GPLv3',
      platforms='any')
