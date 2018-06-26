"""
Visualization and annotation tool for OCT images.
"""

import sys
import traceback
import octlasagne


import os.path as osp


def print_usage():
    print('USAGE:')
    print('python -m octlasange.app <datadir>')
    print('python octlasange.app.py <datadir>')
    print()
    print('EXAMPLE:')
    print('python -m octlasange.app  mydata/octvolumes')


def valid_args():
    if len(sys.argv) != 2:
        print('ERROR: Expect data folder!')
        print_usage()
        return False

    datadir = sys.argv[1]
    if not osp.isdir(datadir):
        print('ERROR: Data folder does not exist: ' + datadir)
        return False

    return True


try:


    if valid_args():
        application = octlasagne.OCTLasagneApp(sys.argv[1])
        application.run()
except:
    application.save_backup()  # Save annotation even when we are crashing
    traceback.print_exc()
