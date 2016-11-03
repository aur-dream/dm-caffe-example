#!/usr/bin/env sh

#################################################
########## Create the dcom lmdb inputs ##########
#################################################

# the following volumes are mounted when the preprocessing container is run:
# - /trainingData (RO)
# - /metadata (RO)
# - /preprocessedData (RW)

# training and validation data stored in same folder
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export PATH=$PATH:/usr/local/cuda/bin
TRAIN_DATA_ROOT=/preprocessedData/data/
LABELS=/preprocessedData/labels
LMDBS=/preprocessedData/lmdbs

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet training data is stored."
  exit 1
fi

echo "Creating train lmdb..."
GLOG_logtostderr=1 caffe_convert_imageset \
    --shuffle \
    --gray=true \
    $TRAIN_DATA_ROOT \
    $LABELS/labels.txt \
    $LMDBS/train_lmdb
echo "Train lmdb creation Done."