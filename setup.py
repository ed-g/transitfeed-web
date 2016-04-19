#!/usr/bin/env python2
from setuptools import setup, find_packages
setup(
    name = "transitfeed_web",
    version = "0.09",
    packages = find_packages(),
    package_dir = {'': '.'},
    include_package_data = True,
    # packages = ['transitfeed_web'],

    # setup_requires = [],
    install_requires = ['transitfeed', 'flask', 'requests', 'requests-ftp'
                      , 'ndg-httpsclient', 'pytz'],

    entry_points = {
        'console_scripts': 
        [ 'transitfeed_web_server = transitfeed_web.run_transitfeed_web_server:main' ],
    },

    author = "Ed",
    author_email = "info@groth-geodata.com",
    description = "GTFS transitfeed and FeedValidator web service",
    license = "Apache 2.0",
    keywords = "gtfs transit",
    url = "http://github.com/ed-g/transitfeed_web",
)
