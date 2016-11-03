#!/usr/bin/env sh

###########################################
########## Create the mean image ##########
###########################################
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export PATH=$PATH:/usr/local/cuda/bin
#LD_LIBRARY_PATH=/usr/local/cuda-6.5/lib64:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
LMDBS=/preprocessedData/lmdbs/

caffe_compute_image_mean $LMDBS/train_lmdb $LMDBS/mean.binaryproto
echo "Mean image creation Done".