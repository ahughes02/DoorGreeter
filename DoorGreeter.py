# Last Updated: 2016-06-15 by Austin Hughes
# Designed for Raspberry Pi 2 running Raspbian
#################################################
#                DoorGreeter.py                 #
#################################################
# Uses a connected sensor to play sounds when a door is opened. 
# Expects input = 1 door is open, 0 door is closed.
# Expects sensor input to be on pin 7.

import os
import sys
import time
import random
import subprocess
import traceback

# This function will return the full path to all .mp3s in the directory
def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            # Only save mp3 files
            if filepath.endswith(".mp3"): 
                file_paths.append(filepath)  # Add it to the list.
    return file_paths

try:
    # We need this to access GPIO pins
    import RPi.GPIO as GPIO
    try:
        t = 21 # time to sleep
        loop = 1 # controls loop in future could set to 0 to break out of loop
        stillOpen = 0 # Don't keep playing if the door is still open

        # Always be looping
        while loop:
            # Set up GPIO mode
            GPIO.setmode(GPIO.BOARD)
            # Setup the input
            GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
            # get the input
            input = GPIO.input(7)
            # Reset the GPIO Pins
            GPIO.cleanup()

            # Check if the door has been closed
            if stillOpen == 1 and input == 0:
                stillOpen = 0
            # If it hasn't, don't play a sound
            elif stillOpen == 1 and input == 1:
                input = 0

            # If the door is open play a sound
            if input == 1:
                # Log what we are doing
                print "Target dir: ", sys.argv[1]
                try:
                    # Get the files
                    filepaths = get_filepaths(sys.argv[1])
                    # If we found files on the path
                    if(len(filepaths) > 0):
                        # Log
                        print "Found", len(filepaths), "files"
                        # Pick a file
                        file = random.choice(filepaths)
                        # Log
                        print "Playing file", filepaths.index(file)
                        print file
                        # Generate the command to play audio, change local to HDMI to play over HDMI
                        command = "omxplayer -o local " + file
                        # Run it
                        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                        # Sleep for t seconds
                        time.sleep(t)
                        # Set still open to true
                        stillOpen = 1
                    # Otherwise we don't have files, log it
                    else:
                        print "No .mp3 files found"
                # Log the exception
                except:
                    traceback.print_exc()
            # Sleep for a bit
            time.sleep(.25)
    # Log that we didn't get an argument
    except:
        print "Please provide a path to target .mp3 files"
# Log exceptions
except RuntimeError:
    print("Error importing RPi.GPIO!")
    traceback.print_exc()