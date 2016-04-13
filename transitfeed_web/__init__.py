#!/usr/bin/env python2

import sys

import transitfeed

def main():
    schedule = transitfeed.Schedule()
    schedule.AddAgency("Fly Agency", "http://iflyagency.com",
                       "America/Los_Angeles")

    schedule.WriteGoogleTransitFeed('google_transit.zip')

if __name__ == '__main__':
    main()

