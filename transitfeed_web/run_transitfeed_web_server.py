#!/usr/bin/env python2

import sys
import transitfeed
import time # for testing
import cStringIO #write GTFS directly to network.
from hexdump import hexdump

def main():
    schedule = transitfeed.Schedule()
    schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                       "America/Los_Angeles")

    gtfs_stringio = cStringIO.StringIO()

    # schedule.WriteGoogleTransitFeed('test_transitfeed_web.gtfs.zip')
    schedule.WriteGoogleTransitFeed(gtfs_stringio)

    while True:
        time.sleep(3)
        print("Hello, from transitfeed_web server.")
        print("Hexdump of GTFS.")
        hexdump(gtfs_stringio.getvalue())

if __name__ == '__main__':
    main()
