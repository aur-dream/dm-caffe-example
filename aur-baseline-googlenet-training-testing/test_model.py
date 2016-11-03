#!/usr/bin/env python

###############################################################################################
# This script predicts cancer positive probabilities (for each breast) from a trained model.  #
# Outputs predictions in format: Sage_ID | Laterality | cancer_positive_probability           #
# Author(s):    syohan@au1.ibm.com, umarasif@au1.ibm.com                                      #
# Last updated: 05OCT16                                                                       #
###############################################################################################

import csv
import numpy as np
import random
import caffe
import itertools

TEST = False # True = test on 100 images; False = full set
MEAN_BINPROTO = '/preprocessedData/lmdbs/mean.binaryproto'
MEAN_NPY = '/mean.binaryproto.npy'
VAL_DATA = '/modelState/preprocessedData/'
MODEL_FILE1 = '/deploy.prototxt'
OUTPUT = '/modelState/out.txt'
CROSSWALK = '/metadata/sc1_images_crosswalk.tsv'

print "Setting GPU mode..."
#caffe.set_device(0)
caffe.set_mode_gpu() # uses single available gpu
print "GPU mode set."
print "Converting mean.binaryproto to npy..."
print "Creating blob..."
blob = caffe.proto.caffe_pb2.BlobProto()
print "Blob created."
data = open(MEAN_BINPROTO, 'rb').read()
blob.ParseFromString(data)
print "Converting blob to array..."
arr = np.array(caffe.io.blobproto_to_array(blob))
out = arr[0]
print "Saving mean.binaryproto.npy..."
np.save(MEAN_NPY, out)
print "mean.binaryproto.npy created."

# test model and generate predictions

if TEST:
    PRETRAINED1 = '/modelState/caffe_googlenet_iter_7.caffemodel'
else:
    PRETRAINED1 = '/modelState/caffe_googlenet_iter_200000.caffemodel'

print "Creating prediction model..."
net1 = caffe.Classifier(MODEL_FILE1, PRETRAINED1, mean = \
                        np.load(MEAN_NPY).mean(1).mean(1),channel_swap=[0],\
                        raw_scale=255,image_dims=(500,500))
print "Prediction model created."

crosswalk = open(CROSSWALK, 'rb')
crosswalk = csv.DictReader(crosswalk, delimiter = '\t') 
p_ids = []    
laterality = [] 
scores = []

print "Iterating Crosswalk data and generating predictions..."
count = 0

if TEST:
    rows = itertools.islice(crosswalk, 368, 468)
else:
    rows = crosswalk
    
for line in rows:
    if line['subjectId'] == 'subjectId':
        continue # ignore headers
    else:
        filename = line['filename']
        filename =  filename[:-4]
        filepath = VAL_DATA + filename + '.png'
        # Loading image into Caffe...
        img = caffe.io.load_image(filepath, False) # False = greyscale
        # Predicting score...
        score = net1.predict([img])
        p_ids.append(int(line['subjectId']))
        laterality.append(line['laterality'])
        scores.append(score[0][1])

print "Pooling predictions..."
unique_ids = list(set(p_ids))
with open(OUTPUT,'wb') as output_f:
    for i in range(0,len(unique_ids)):
        try:
            p_id = unique_ids[i]
            indices = [j for j, x in enumerate(p_ids) if x == p_id]
            laterls = [laterality[k] for k in indices]
            scores1 = [scores[k] for k in indices]
            indices_R = [j for j, x in enumerate(laterls) if x == 'R']
            indices_L = [j for j, x in enumerate(laterls) if x == 'L']

            scores_R = [scores1[k] for k in indices_R]
            scores_L = [scores1[k] for k in indices_L]
            scores_R = np.max(scores_R)
            scores_L = np.max(scores_L)
            item = str(p_id)+'\t'+ laterls[indices_R[0]]+'\t'+ str(scores_R)
            output_f.write('%s\n' % item)
            item = str(p_id)+'\t'+ laterls[indices_L[0]]+'\t'+ str(scores_L)
            output_f.write('%s\n' % item)
        except IOError as e:
            print e
            continue
        except ValueError:
            print "Could not convert data to an integer."
            continue

print("out.txt generated.")
