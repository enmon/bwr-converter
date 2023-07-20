#
# rle_encoder.py
# Functions to compress/decompress images using a simple RLE-based format
#
# A simple bytewise RLE compression format is used:
# XYVVVVVV
#  X=0 -> YVVVVVV are the bit values of the next 7 pixels (or padding if the row ends)
#  X=1 -> the next (0bVVVVVV + 1) pixels shall have bit value Y
#
# Copyright (C) 2023 rw-r-r-0644
# This file is under MIT license
#
import numpy as np

def _encode_block(arr):
    # lookup the next 7 pixels
    lookup = arr[:7]

    # decide whether RLE or direct encoding shall be used
    prefix = None
    if np.all(lookup == 0):
        prefix = 0
    elif np.all(lookup == 1):
        prefix = 1

    # encode pixels
    if prefix == None:
        count = 7
        encoded = np.packbits(np.append(0, lookup))[0]
    else:
        diff = np.nonzero(arr != prefix)[0]
        count = min(64, diff[0] if diff.size > 0 else arr.size)
        encoded = 0x80 | (prefix << 6) | (count - 1)

    return count, encoded

def _encode_row(row):
    row_enc = []
    x = 0
    while x < row.size:
        count, enc = _encode_block(row[x:])
        row_enc.append(enc)
        x += count
    return row_enc

def rle_encode(img_arr):
    enc = []
    for row in img_arr:
        enc += _encode_row(row)
    return np.array(enc, dtype=np.uint8)

def _decode_block(b):
    if b & 0x80:
        return np.array([(b >> 6) & 1] * ((b & 63) + 1))
    else:
        return np.unpackbits(np.array([b], dtype=np.uint8))[1:]

def _decode_row(arr, width):
    row = []
    count = 0
    while len(row) < width:
        row += _decode_block(arr[count])
        count += 1
    return count, row

def rle_decode(rle_arr, width):
    rows = []
    offs = 0
    while offs < rle_arr.size:
        count, row = _decode_row(arr[offs:])
        offs += count
        rows.append(row)
    return numpy.array(rows, dtype=np.uint8)
