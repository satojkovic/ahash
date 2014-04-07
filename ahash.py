#-*- coding: utf-8 -*-

"""
Usage: ahash.py <IMAGE>
       ahash.py -h | --help
       ahash.py --version
Options:
       -h --help    show this screen
       --version    show version
"""

from docopt import docopt
import sys
import cv2

RESIZE_W = 8
RESIZE_H = 8


def main():
    opts = docopt(__doc__, version='1.0')
    img_file = opts['<IMAGE>']
    if not img_file:
        print 'Not found: %s' % img_file
        sys.exit(1)

    # read the image
    img = cv2.imread(img_file)

    # Reduce size
    img = cv2.resize(img, (RESIZE_W, RESIZE_H))

    # Reduce color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Average the color
    img_mean = cv2.mean(img)[0]

    # Compute the bits
    bits = img > img_mean

    # Construct the hash
    h = 0
    ahash = []
    for i, v in enumerate(bits.flatten()):
        if v:
            h += 2**(i % 8)
        if (i % 8) == 7:
            ahash.append(hex(h)[2:].rjust(2, '0'))
            h = 0

    print 'ahash = %s' % ''.join(ahash)

if __name__ == '__main__':
    main()
