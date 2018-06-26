"""
Common functions.
"""

import csv

import pickle as pkl
import pandas as pd

from kivy.uix.popup import Popup
from kivy.uix.label import Label


def parse_anno(text):
    """Convert text with layer annotation to data structure"""
    return eval(text) if text else None


def layernames_from_csv(filepath):
    """Read first line of CSV file and return list of layer names in header"""
    with open(filepath) as f:
        reader = csv.reader(f)
        header = next(reader)
        return [n for n in header if n[:2] == 'l:']


def load_from_csv(filepath):
    """Read dataframe from CSV file"""
    layernames = layernames_from_csv(filepath)
    converters = {n: parse_anno for n in layernames}
    df = pd.read_csv(filepath, converters=converters)
    return df


def save_as_csv(df, filepath):
    """Save dataframe as CSV file"""
    df.to_csv(filepath, index=False)


def load_from_pickle(filepath):
    """Read dataframe from pickle file"""
    return pd.read_pickle(filepath)


def save_as_pickle(df, filepath, compression='infer', protocol=2):
    """
    Pickle (serialize) object to given file path.
    Original implementation in pandas.pickle. Modified to ensure pickle files
    written can be read with Python 2.x and Python 3.x

    :param DataFrame df:  Pandas data frame
    :param str filepath: File path
    :param str compression : One of 'infer', 'gzip', 'bz2', 'xz', None,
                              default 'infer'
    :param int protocol : pickle protocol used, e.g. pkl.HIGHEST_PROTOCOL
    """
    from pandas.io.common import _get_handle, _infer_compression
    inferred_compression = _infer_compression(filepath, compression)
    f, fh = _get_handle(filepath, 'wb',
                        compression=inferred_compression,
                        is_text=False)
    try:
        pkl.dump(df, f, protocol=protocol)
    finally:
        for _f in fh:
            _f.close()


def load_dataframe(filepath):
    """Load dataframe from CSV or PICKLE file"""
    if filepath.endswith('.csv'):
        return load_from_csv(filepath)
    if filepath.endswith('.pkl'):
        return load_from_pickle(filepath)
    raise ValueError('Unsupported filetype: ' + filepath)


def save_dataframe(df, filepath):
    """Save dataframe to CSV or PICKLE file"""
    if filepath.endswith('.csv'):
        return save_as_csv(df, filepath)
    if filepath.endswith('.pkl'):
        return save_as_pickle(df, filepath)
    raise ValueError('Unsupported filetype: ' + filepath)
