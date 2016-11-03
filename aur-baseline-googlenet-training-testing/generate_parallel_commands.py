#!/usr/bin/env python

#####################################################################################
# This script generates the following files:                                        #
# - parallel_commands_preprocess.txt: input file for GNU parallel for preprocessing #
# - parallel_commands_resize.txt: input file for GNU parallel to resize images      #
# Author:       syohan@au1.ibm.com                                                  #
# Last updated: 05OCT16                                                             #
#####################################################################################

import csv
import itertools
import numpy as np

TEST = False # True = test on 100 images; False = full set
CROSSWALK_FILE = '/metadata/sc1_images_crosswalk.tsv'
PARALLEL_COMMANDS_PREPROCESS_FILE = '/parallel_commands_preprocess.txt'
PARALLEL_COMMANDS_RESIZE_FILE = '/parallel_commands_resize.txt'
SPLIT_DELIMITER = '\t'

print 'Generating parallel_commands_preprocess.txt...'
print 'Generating parallel_commands_resize.txt...'
# Generate labels
with open(CROSSWALK_FILE, 'rb') as crosswalk_f, \
     open(PARALLEL_COMMANDS_PREPROCESS_FILE, 'wb') as parallel_commands_preprocess_f, \
     open(PARALLEL_COMMANDS_RESIZE_FILE, 'wb') as parallel_commands_resize_f:
    reader = csv.DictReader(crosswalk_f, delimiter = SPLIT_DELIMITER)

    if TEST:
        rows = itertools.islice(reader, 368, 468)
    else:
        rows = reader
        
    for row in rows:
        filename = row['filename']
        parallel_commands_preprocess_f.write('python preprocess_dm_images.py /sc1ScoringData/' \
            + filename + ' /modelState/preprocessedData/' + filename[:-3] + 'png; convert -resize 500x500! /modelState/preprocessedData/' \
            + filename[:-3] + 'png' + ' /modelState/preprocessedData/' + filename[:-3] + 'png\n')
##        parallel_commands_resize_f.write('convert -resize 500x500! /modelState/preprocessedData/' \
##            + filename[:-3] + 'png' + ' /modelState/preprocessedData/' + filename[:-3] + 'png\n')

    print 'parallel_commands_preprocess.txt generated.'
    print 'parallel_commands_resize.txt generated.'
