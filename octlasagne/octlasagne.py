"""
Visualization and annotation tool for OCT images.
"""

import sys
import traceback
import octapp

import os.path as osp


def print_usage():
    print('USAGE:')
    print('python octlasagne.py <datadir> [-s <width_scale>]')
    print()
    print('EXAMPLES:')
    print('python octlasagne.py  mydata/octvolumes')
    print('python octlasagne.py  mydata/octvolumes -s 0.5')


def parse_args(argv):
    invalid = (None, None)

    if len(argv) not in {2, 4}:
        print('ERROR: Invalid arguments!')
        print_usage()
        return invalid

    width_scale = float(argv[3]) if len(argv) == 4 else 1.0
    if len(argv) == 4 and argv[2] != '-s':
        print('ERROR: Expected parameter -s')
        print_usage()
        return invalid

    datadir = argv[1]
    if not osp.isdir(datadir):
        print('ERROR: Data folder does not exist: ' + datadir)
        return invalid

    return datadir, width_scale


if __name__ == '__main__':
    try:
        datadir, width_scale = parse_args(sys.argv)
        if datadir and width_scale:
            application = octapp.OCTLasagneApp(datadir, width_scale)
            application.run()
    except:
        application.save_backup()  # Save annotation even when we are crashing
        traceback.print_exc()
