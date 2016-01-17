#!/usr/bin/env python3


import logging
import signal
import datetime
import time
import math
import argparse
import sys
import os
import json
from enum import Enum

SECONDS_IN_DAY = 86400

class RunMode(Enum):
    SCHEDULED   = 1
    ONCE        = 2
    DOWNLOAD    = 3
    BACKTEST    = 4
    REPORT      = 5


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Throws exceptions on interrupt signals
def interrupt(num, frame):
    logging.debug("Signal caught: ", num)
    # raise OSError("Caught signal (", num, ")")

   
# Hook signals
signal.signal(signal.SIGINT, interrupt)
signal.signal(signal.SIGTERM, interrupt)

def run(mode):
    '''Execute a single task, according to the mode'''
    if mode in (RunMode.ONCE, RunMode.SCHEDULED, RunMode.DOWNLOAD):
        # TODO: update task
        pass
    
    if mode == RunMode.BACKTEST:
        # TODO: backtest task
        pass

    if mode in (RunMode.ONCE, RunMode.SCHEDULED, RunMode.REPORT):
        # TODO: render/send report
        pass


def dispatch():
    '''Dispatch processing events at midnight every night'''
    while True:
        now           = time.time()
        next_midnight = math.ceil(now / SECONDS_IN_DAY) * SECONDS_IN_DAY 
        delay         = math.ceil(next_midnight - now)

        logging.info("Waiting %s seconds until %s" 
                % (delay, datetime.datetime.fromtimestamp(next_midnight)))
        signal.alarm(delay)
        signum = signal.sigwait([signal.SIGALRM, signal.SIGINT, signal.SIGTERM])

        if signum == signal.SIGALRM:
            logging.info("Starting work")
            run()
        else:
            logging.info("Exit requested")
            break



def load_config(fpath):
    '''Load the config file from a path provided, and return it as a Namespace'''

    logging.info("Loading config from filename: %s" % (fpath))

    fh = open(fpath, 'r')
    config = json.loads(fh.read())
    fh.close

    return config


def main():

    parser = argparse.ArgumentParser(description='Stock monitor daemon')

    parser.add_argument('-c', '--config', nargs=1, default='config.json',
            help='The JSON config file path')
    parser.add_argument('mode', metavar='MODE', nargs=1, default='SCHEDULED',
            choices=['ONCE', 'SCHEDULED', 'DOWNLOAD', 'BACKTEST', 'REPORT'],
            help='The run mode')

    opts = parser.parse_args() 
    mode = RunMode[opts.mode[0]]
    conf = load_config(opts.config)
    logging.info("Starting in mode: %s" % (mode))

    # Run dispatch task
    if mode == RunMode.SCHEDULED:
        dispatch()
    else:
        run(mode)

    logging.info("Clean exit.")
    sys.exit(0)


if __name__ == "__main__":
    main()



