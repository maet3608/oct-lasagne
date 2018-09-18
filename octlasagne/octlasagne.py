"""
Visualization and annotation tool for OCT images.
"""

import sys
import json
import traceback
import octapp

import os.path as osp


def print_usage():
    print('USAGE:')
    print('python octlasagne.py <config_file')
    print()
    print('EXAMPLE:')
    print('python octlasagne.py  config.json')


def parse_args(argv):
    if len(argv) != 2:
        print('ERROR: Missing configuration file argument!')
        print_usage()
        return None

    configpath = argv[1]
    if not osp.exists(configpath):
        print('ERROR: Configuration files does not exist: ' + configpath)
        return None

    with open(configpath) as f:
        config = json.load(f)

    return config


if __name__ == '__main__':
    try:
        config = parse_args(sys.argv)
        if config:
            application = octapp.OCTLasagneApp(config)
            application.run()
    except:
        application.save_backup()  # Save annotation even when we are crashing
        traceback.print_exc()
