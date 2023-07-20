## bwr_converter
Prepares black/white/red images for visualization on ePaper displays with the Adafruit GFX library:  
* given `inputname.bmp`  
* split the image in black channel and red channel monochrome images  
* convert both monochrome images to Adafruit GFX 1-bit bitmap representation:  
    - by-row ordering  
    - leftmost bits as MSB  
    - byte-aligned row start  
* output the images to `inputname.c` as `inputname_width`, `inputname_height`, `inputname_black[]`, `inputname_red[]`  

