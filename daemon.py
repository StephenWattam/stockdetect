#!/usr/bin/env python3


import logging
import signal
import datetime
import time
import math
import getopt
import sys
import os

SECONDS_IN_DAY = 86400



# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Throws exceptions on interrupt signals
def interrupt(num, frame):
    logging.debug("Signal caught: ", num)
    # raise OSError("Caught signal (", num, ")")

   
# Hook signals
signal.signal(signal.SIGINT, interrupt)
signal.signal(signal.SIGTERM, interrupt)


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
        else:
            logging.info("Exit requested")
            break




def usage():
    '''Displays usage for getopt.'''
    print("Stock monitor daemon.")
    print()
    print("USAGE: ", os.path.basename(__file__));
    print()



def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    # Run dispatch task
    dispatch() 


if __name__ == "__main__":
    main()



