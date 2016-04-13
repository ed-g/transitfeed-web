from setuptools import setup, find_packages
setup(
    name = "transitfeed-web",
    version = "0.02",
    packages = find_packages(),

    # setup_requires = ['transitfeed', 'flask'],
    install_requires = ['transitfeed', 'flask'],

    author = "Ed",
    author_email = "info@groth-geodata.com",
    description = "GTFS transitfeed and FeedValidator web service",
    license = "Apache 2.0",
    keywords = "gtfs transit",
    url = "http://github.com/ed-g/transitfeed-web",
)
