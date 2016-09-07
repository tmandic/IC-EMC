try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description'       : 'Python library for GPIB in IC-EMC lab at FER.',
    'author'            : 'Marko Magerl',
    'url'               : 'https://github.com/tmandic/IC-EMC',
    'download_url'      : 'https://github.com/tmandic/IC-EMC',
    'author_email'      : 'marko.magerl@fer.hr',
    'version'           : '0.1',
    'install_requires'  : ['nose'],
    'packages'          : ['emclab'],
    'scripts'           : [],
    'name'              : 'emclab'
}

setup(**config)
