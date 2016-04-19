#!/usr/bin/env python2

from __future__ import print_function
import sys
import os
import transitfeed
import time # for testing
import StringIO #write GTFS directly to network.
import requests

# https://github.com/Lukasa/requests-ftp
#
# Requests-FTP is an implementation of a very stupid FTP transport adapter for
# use with the awesome Requests Python library.
# 
# This library is not intended to be an example of Transport Adapters best
# practices. This library was cowboyed together in about 4 hours of total work,
# has no tests, and relies on a few ugly hacks. Instead, it is intended as both
# a starting point for future development and a useful example for how to
# implement transport adapters.
import requests_ftp
requests_ftp.monkeypatch_session()

from flask import Flask, request, url_for, render_template
import re
import json

import util # Actually, transitfeed_web.util

def find_feedvalidator_script_and_add_to_pythonpath():
    # The transitfeed library installs feedvalidator.py in bin/ and its features
    # are not available as a library. So we gotta get creative to import it.
    # Find in which directory is our transitfeed.py file.
    feedvalidator_file = util.search_path('feedvalidator.py')
    feedvalidator_dir  = os.path.dirname(feedvalidator_file)
    #print ("feedvalidator_file: %s" % feedvalidator_file)
    #print ("feedvalidator_dir: %s" %  feedvalidator_dir)

    # And add that sucker to our PYTHONPATH.
    sys.path.append(feedvalidator_dir)

find_feedvalidator_script_and_add_to_pythonpath()
import feedvalidator

def fetch_config_json():
    config_url = os.environ.get('TRANSITFEED_WEB_CONFIG_URL')
    if config_url:
        print ("Fetching config json from  %s" % config_url)
        s = requests.Session() # This is actually monkeypatched requests_ftp Session.
        r = s.get(config_url)
        config = r.json()
    else:
        config = json.loads("""{
                "comment": "This is a configuration file for https://github.com/ed-g/transitfeed_web",
                "regexp_allowlist": [
                    "https://developers.google.com/transit/gtfs/examples/sample-feed.zip" ] } """)
    print ("Config json: %s" % config)
    return config

def url_allowed(config, url):
    allowlist = config['regexp_allowlist']
    print ("allowlist is: %s" % allowlist)
    for a in allowlist:
        if re.match(a, url):
            return True
    return False

CONFIG = fetch_config_json()


app = Flask(__name__)

# server white list -- oregon-gtfs.com data.trilliumtransit.com
# testing_gtfs_url = 'http://oregon-gtfs.com/gtfs_data/tillamook-or-us/tillamook-or-us.zip'
testing_gtfs_url = 'https://developers.google.com/transit/gtfs/examples/sample-feed.zip'

@app.route("/transitfeed_web/validate", methods = ['GET','POST'])
def validate_gtfs_from_url():
    if request.method == 'POST' and request.files['gtfs_file_upload']:
        print("validate_gtfs_from_url: user uploaded a file using POST.", file=sys.stderr)
        gtfs_file = request.files['gtfs_file_upload']

    else:
        gtfs_url = request.form.get("gtfs_url") or request.args.get("gtfs_url") or testing_gtfs_url

        if not url_allowed(CONFIG, gtfs_url):
            # app.logger.warning("validate_gtfs_from_url: Sorry, URL %s is not on our allow-list.", gtfs_url)
            print("validate_gtfs_from_url: Sorry, URL %s is not on our allow-list." % gtfs_url, file=sys.stderr)
            return ("Sorry, URL %s is not on our allow-list." % gtfs_url)

        #app.logger.warning("validate_gtfs_from_url: fetching URL %s", gtfs_url)
        print("validate_gtfs_from_url: fetching URL %s" % gtfs_url, file=sys.stderr)

        s = requests.Session() # This is actually monkeypatched requests_ftp Session.
        r = s.get(gtfs_url)

        gtfs_file = StringIO.StringIO()
        gtfs_file.write(r.content) # binary content in r.content 
        gtfs_file.seek(0) #rewind.

    # Pretend to pass command-line arguments to feedvalidator. It returns an
    # "options" object which is used to configure to the validation function.
    save_argv = sys.argv  # save actual argv
    sys.argv = ['fakeout-argv-for-feedparser.py', 'fake-placeholder-gtfs-file.zip']
    options = feedvalidator.ParseCommandLineArguments()[1]
    sys.argv = save_argv  # restore argv

    output_file = StringIO.StringIO()
    feedvalidator.RunValidationOutputToFile(gtfs_file,options,output_file)

    return output_file.getvalue()


@app.route("/transitfeed_web/test-gtfs.zip")
def test_gtfs_output():
    schedule = transitfeed.Schedule()
    schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                       "America/Los_Angeles")

    gtfs_stringio = StringIO.StringIO()
    schedule.WriteGoogleTransitFeed(gtfs_stringio)
    return gtfs_stringio.getvalue()

@app.route("/")
@app.route("/transitfeed_web/")
def index():
    return render_template('index.html')

def main():
    # Never use debug=True in production, it's completely insecure.
    # app.run(host='0.0.0.0', port=5000, debug=True) ## 
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
