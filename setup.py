#!/usr/bin/env python2
from setuptools import setup, find_packages
setup(
    name = "transitfeed_web",
    version = "0.02",
    packages = find_packages(),

    # setup_requires = ['transitfeed', 'flask'],
    install_requires = ['transitfeed', 'flask'],

    entry_points = {
        'console_scripts': 
          [ 'transitfeed_web = transitfeed_web:main' ],
    },

    author = "Ed",
    author_email = "info@groth-geodata.com",
    description = "GTFS transitfeed and FeedValidator web service",
    license = "Apache 2.0",
    keywords = "gtfs transit",
    url = "http://github.com/ed-g/transitfeed-web",
)
