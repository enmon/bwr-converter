#
# bwr_converter.py
# Prepares black/white/red images for visualization on
# ePaper displays with the Adafruit GFX library
#
# Copyright (C) 2023 rw-r-r-0644
# This file is under MIT license
#
#!/bin/python3
from PIL import Image
import numpy as np
import argparse
from os import path

def monochrome_color(img, color):
    masked = np.all(img == color, axis=-1)
    return np.packbits(masked, axis=1).flatten()

def to_hex(barray, elmhdr='0x', elmsep=',', rowsep=',\n', rowhdr='', rowsz=16):
    rows = []
    for i in range(0, barray.size, rowsz):
        rows.append(rowhdr + elmsep.join(f'{elmhdr}{b:02X}' for b in barray[i:i+rowsz]))
    return rowsep.join(rows)

def bwr_convert(in_path, out_path, name):
    img = Image.open(in_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    width, height = img.size
    img_arr = np.asarray(img)

    black_bitmap = monochrome_color(img_arr, [0x00, 0x00, 0x00])
    red_bitmap = monochrome_color(img_arr, [0xff, 0x00, 0x00])

    with open(out_path, 'w') as f:
        f.write(('const unsigned int\n'
            f'{name}_width = {width},\n'
            f'{name}_height = {height};\n\n'
            'const unsigned char\n'
            f'{name}_black[] = {{\n{to_hex(black_bitmap)}\n}},\n'
            f'{name}_red[] = {{\n{to_hex(red_bitmap)}\n}};\n'
        ))

def main():
    parser = argparse.ArgumentParser(prog='bwr_converter.py',
        description=('Prepares black/white/red images for visualization\n'
                     'on ePaper displays with the Adafruit GFX library'))
    parser.add_argument('filename')
    args = parser.parse_args()

    in_basepath = path.splitext(args.filename)[0]
    bwr_convert(args.filename,
        in_basepath + '.c',
        path.basename(in_basepath))

if __name__ == "__main__":
    main()
