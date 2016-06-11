# Last Updated: 2016-06-10 by Austin Hughes
import sys
import os
import random
import subprocess

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
    print "Target dir: ", sys.argv[1]
    try:
        filepaths = get_filepaths(sys.argv[1])
        if(len(filepaths) > 0):
            print "Found", len(filepaths), "files"
            file = random.choice(filepaths)
            print "Playing file", filepaths.index(file)
            print file
            command = "omxplayer -o local " + file
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        else:
            print "No .mp3 files found"

    except:
        e = sys.exc_info()[0]
        print "Exception: "
        print e
except:
    print "Please provide a path to target .mp3 files"