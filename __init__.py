#!/usr/bin/env python2

import sys

import transitfeed

if __name__ == '__main__':
    schedule = transitfeed.Schedule()
    schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                       "America/Los_Angeles")

    schedule.WriteGoogleTransitFeed('google_transit.zip')
