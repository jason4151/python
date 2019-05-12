#!/usr/bin/python

import tarfile, sys

try:
    # Open tarfile
    tar = tarfile.open(sys.argv[1], "r:tar")

    # Present menu and get selection
    selection = raw_input("Enter\n\
    1 to extract a file\n\
    2 to display information on a file in the archive\n\
    3 to list all the files in the archive\n\n")

    # Perform actions based on selection above
    if selection == "1":
        filename = raw_input("enter the filename to extract:  ")
        tar.extract(filename)
    elif selection == "2":
        filename = raw_input("enter the filename to inspect:  ")
        for tarinfo in tar:
            if tarinfo.name == filename:
                print "\nFilename:\t\t", tarinfo.name, "\nSize:\t\t", tarinfo.size, "bytes\n"
    elif selection == "3":
        print tar.list(verbose=True)
except:
    print "There was a problem running the program"
