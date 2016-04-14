#!/usr/bin/env python2

import sys
import os
import transitfeed
import time # for testing
import StringIO #write GTFS directly to network.
import hexdump 
import requests
from flask import Flask

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

app = Flask(__name__)

testing_gtfs_url = 'http://oregon-gtfs.com/gtfs_data/tillamook-or-us/tillamook-or-us.zip'

class FakeOptions:
    def __init__(options):
        # options = {} #How can we create empty Python object??
        options.manual_entry=True
        # options.output='validation-results.html',
        options.memory_db=False
        options.check_duplicate_trips=False,
        options.limit_per_type=5
        # options.latest_version='1.2.1',
        options.latest_version=None, ## FIXME. this is causing problems.
        options.service_gap_interval=13
        options.error_types_ignore_list = ""


@app.route("/validate-demo")
def validate_demo():
    r = requests.get(testing_gtfs_url)
    #return ("length of gtfs file is: %s" % len(r.content))

    gtfs_file = StringIO.StringIO()
    gtfs_file.write(r.content) # binary content in r.content 
    gtfs_file.seek(0) #rewind.

    options = FakeOptions()

    output_file = StringIO.StringIO()

    feedvalidator.RunValidationOutputToFile(gtfs_file,options,output_file)

    return output_file.getvalue()


@app.route("/test-gtfs.zip")
def test_gtfs_output():
    schedule = transitfeed.Schedule()
    schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                       "America/Los_Angeles")

    gtfs_stringio = StringIO.StringIO()
    schedule.WriteGoogleTransitFeed(gtfs_stringio)
    return gtfs_stringio.getvalue()

@app.route("/")
def hello():
    return "Hello, from transitfeed_web server!"


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

def loop_and_print_stuff_for_docker_testing():
    schedule = transitfeed.Schedule()
    schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                       "America/Los_Angeles")

    gtfs_stringio = cStringIO.StringIO()

    # schedule.WriteGoogleTransitFeed('test_transitfeed_web.gtfs.zip')
    schedule.WriteGoogleTransitFeed(gtfs_stringio)

    while True:
        time.sleep(3)
        print("Hello, from transitfeed_web server.")
        print("Running as user: %s group: %s" % ( os.getuid(), os.getgid()))
        print("Hexdump of GTFS.")
        print(hexdump.hexdump(gtfs_stringio.getvalue(), 'return'))

if __name__ == '__main__':
    main()
