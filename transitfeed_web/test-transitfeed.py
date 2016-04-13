#!/usr/bin/env python2

import sys

# we should probably instead be using easy_install to grab our Python
# dependancies, rather than git submodule.
sys.path.append("transitfeed_submodule")

import transitfeed

schedule = transitfeed.Schedule()
schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                   "America/Los_Angeles")

schedule.WriteGoogleTransitFeed('google_transit.zip')
