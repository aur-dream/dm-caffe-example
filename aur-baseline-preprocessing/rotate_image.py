#!/usr/bin/env python

#################################################################################
# This script takes an input image and rotates a copy by some angle.            #
# Author:       syohan@au1.ibm.com                                              #
# Last updated: 28SEP16                                                         #
#################################################################################

import numpy as np
from skimage.transform import rotate
from scipy.misc import imsave
from scipy import misc
import csv
import sys

def rotate_image(inImgFilename, outImgFilename, rotAngle):
    """
    Rotates a copy of inImgFilename by angle rotAngle (in degrees)

    Args:
        inImgFilename (str): path to the input mammogram in PNG format
        outImgFilename (str): directory where the output image must be saved in PNG format
        rotAngle (float): angle to rotate image (in degrees)
    """

    raw = misc.imread(inImgFilename)
    aug = rotate(raw, rotAngle)
    imsave(outImgFilename, aug)

if __name__ == '__main__':
    inImgFilename = sys.argv[1]
    outImgFilename = sys.argv[2]
    rotAngle = float(sys.argv[3])

    #print('Rotating ' + inImgFilename + ' by ' + str(rotAngle) + ' degrees -> ' + outImgFilename)
    rotate_image(inImgFilename, outImgFilename, rotAngle)
