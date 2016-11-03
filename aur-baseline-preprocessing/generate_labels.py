#!/usr/bin/env python

#####################################################################################
# This script generates the following files:                                        #
# - labels.txt: list of filenames and corresponding labels (1=cancer, 0=no cancer). #
# - parallel_commands_preprocess.txt: input file for GNU parallel for preprocessing.#
# - parallel_commands_resize.txt: input file for GNU parallel to resize images.     #
# - parallel_commands_augment.txt: input file for GNU parallel to augment images.   #
# Author:       syohan@au1.ibm.com                                                  #
# Last updated: 05OCT16                                                             #
#####################################################################################

import csv
import itertools
import numpy as np

TEST = False # True = test on 100 images; False = full set
CROSSWALK_FILE = '/metadata/images_crosswalk.tsv'
METADATA_FILE = '/metadata/exams_metadata.tsv'
LABELS_FILE = '/preprocessedData/labels/labels.txt'
PARALLEL_COMMANDS_PREPROCESS_FILE = \
    '/preprocessedData/labels/parallel_commands_preprocess.txt'
PARALLEL_COMMANDS_RESIZE_FILE = \
    '/preprocessedData/labels/parallel_commands_resize.txt'
PARALLEL_COMMANDS_AUGMENT_FILE = \
    '/preprocessedData/labels/parallel_commands_augment.txt'
SPLIT_DELIMITER = '\t'
ROTATION_START = -15 # degrees (both define augmentation range)
ROTATION_END = 15 # degrees
metadata_ht = {}
pos_list = []
neg_count = 0

print 'Generating labels.txt...'
print 'Generating parallel_commands_preprocess.txt...'
print 'Generating parallel_commands_resize.txt...'
# Load metadata_ht
with open(METADATA_FILE, 'rb') as metadata_f:
    reader = csv.DictReader(metadata_f, delimiter = SPLIT_DELIMITER)
    for row in reader:
        keyL = row['subjectId'] + '_' + \
               row['examIndex'] + '_L'
        keyR = row['subjectId'] + '_' + \
               row['examIndex'] + '_R'
        if keyL not in metadata_ht:
            metadata_ht[keyL] = row['cancerL']
        if keyR not in metadata_ht:
            metadata_ht[keyR] = row['cancerR']

# Generate labels
with open(CROSSWALK_FILE, 'rb') as crosswalk_f, \
     open(LABELS_FILE, 'wb') as labels_f, \
     open(PARALLEL_COMMANDS_PREPROCESS_FILE, 'wb') as parallel_commands_preprocess_f, \
     open(PARALLEL_COMMANDS_RESIZE_FILE, 'wb') as parallel_commands_resize_f:
    reader = csv.DictReader(crosswalk_f, delimiter = SPLIT_DELIMITER)

    if TEST:
        rows = itertools.islice(reader, 368, 468)
    else:
        rows = reader

    for row in rows:
        key = row['subjectId'] + '_' + \
              row['examIndex'] + '_' + \
              row['laterality']
        label = metadata_ht[key]
        filename = row['filename']

        if label == '1':
            pos_list.append(filename[:-3] + 'png')
        else:
            neg_count += 1

        labels_f.write(filename[:-3] + 'png' + ' ' + label + '\n')
        parallel_commands_preprocess_f.write('python preprocess_dm_images.py /trainingData/' \
            + filename + ' /preprocessedData/data/' + filename[:-3] + 'png\n')
        parallel_commands_resize_f.write('convert -resize 500x500! /preprocessedData/data/' \
            + filename[:-3] + 'png' + ' /preprocessedData/data/' + filename[:-3] + 'png\n')

    ratio = neg_count / len(pos_list)
    print 'parallel_commands_preprocess.txt generated.'
    print 'parallel_commands_resize.txt generated.'

# iterate pos_list and generate augmentation list
print 'Generating parallel_commands_augment.txt...'
rotations = np.linspace(ROTATION_START, ROTATION_END, num=ratio)
with open(LABELS_FILE, 'ab') as labels_f, \
     open(PARALLEL_COMMANDS_AUGMENT_FILE, 'wb') as parallel_commands_augment_f:
    for filename in pos_list: # filename is .png
        # Generate ratio number of rotations
        for rot in range(len(rotations)):
            aug_filename = str(rot) + '_' + filename
            parallel_commands_augment_f.write('python rotate_image.py /preprocessedData/data/' \
                + filename + ' /preprocessedData/data/' \
                + aug_filename + ' ' + str(rotations[rot]) + '\n')
            # Save this record (filename & positive label) to labels.txt
            labels_f.write(aug_filename + ' 1\n')
    print 'parallel_commands_augment.txt generated.'
    print 'labels.txt generated.'
    
