import os
import time
import datetime as dt
from sense_energy import Senseable
from sense_energy.sense_exceptions import SenseAPITimeoutException
import numpy as np
from scipy.ndimage import uniform_filter1d
import logging


########################################################################################
# configuration
########################################################################################
logging.basicConfig(level=logging.DEBUG)

# use 60 and 5 = read every minute and average over 5 minutes
interval_between_readings = 60
intervals_for_average = 5


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, required=True)
parser.add_argument('--password', type=str, required=True)
args = parser.parse_args()


########################################################################################
# initialize
########################################################################################

sense = Senseable()
sense.authenticate(args.username, args.password)
sense.update_realtime()

# initialize as intervals_for_average len with zeros
readings = [0] * intervals_for_average

########################################################################################
# main loop
########################################################################################

while True:
    
    # read meter
    try:
        sense.update_realtime()
    except SenseAPITimeoutException:
        logging.error(err)

    # calculate current net and moving average
    net_flow_now = sense.active_solar_power - sense.active_power
    readings.append(net_flow_now)
    average_net_flow = uniform_filter1d(readings, size=intervals_for_average)

    now = dt.datetime.now().isoformat(timespec='seconds')
    
    # output message
    print(f"{now}: Average net flow to grid is over last {intervals_for_average} minutes is {net_flow_now:.0f} watts. ")

    #truncate the readings list if longer than intervals_for_average
    if len(readings) > intervals_for_average:
        readings = readings[-intervals_for_average:]

    # wait until next scheduled reading 
    time.sleep(interval_between_readings)
    




