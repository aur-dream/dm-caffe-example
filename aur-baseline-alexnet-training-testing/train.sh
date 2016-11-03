#!/usr/bin/env sh

##############################################
########## RUN THE TRAINING ROUTINE ##########
##############################################

# The following volumes are mounted when the preprocessing container is run:
# - /metadata (RO)
# - /modelState (RW)
# - /preprocessedData (RO)
# furthermore, /metadata contains the following files:
# - /metadata/exams_metadata.tsv
# - /metadata/images_crosswalk.tsv

# Train a GoogLeNet model using preprocessed data (available in /preprocessedData/data)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
export PATH=$PATH:/usr/local/cuda/bin
#MODEL=/test_solver.prototxt # Test on 100 images
MODEL=/full_solver.prototxt # Full set

echo '['$(date)']:' "Training GoogLeNet..."
caffe train --solver=$MODEL --gpu=all
echo '['$(date)']:' "AlexNet training complete."

#############################################
########## RUN THE SCORING ROUTINE ##########
#############################################

# create sub dir for temp storing preprocessed scoring data
mkdir -p /modelState/preprocessedData
echo '['$(date)']:' "/modelState/preprocessedData folder created."

# generate:
# - labels.txt
# - parallel_commands_preprocess.txt
# - parallel_commands_resize.txt
echo '['$(date)']:' "Generating parallel commands..."
python generate_parallel_commands.py
echo '['$(date)']:' "parallel commands generated."

# parallel convert DICOMs to PNGs & apply preprocessing
echo '['$(date)']:' "Converting DICOMs to PNGs..."
sudo ln /dev/null /dev/raw1394
parallel -k < parallel_commands_preprocess.txt
echo '['$(date)']:' "DICOM to PNG conversion done."

# parallel resize preprocessed PNGs
#echo '['$(date)']:' "Resizing images..."
#parallel < parallel_commands_resize.txt
#echo '['$(date)']:' "Resizing done."

# Test the trained GoogLeNet model using test data (available in /preprocessedData/data)

echo '['$(date)']:' "Testing AlexNet..."
python test_model.py
echo '['$(date)']:' "AlexNet testing complete."

# Clean-up
echo '['$(date)']:' "Cleaning up..."
rm -rf /modelState/preprocessedData
#rm -rf /modelState/caffe_alexnet_iter_200000.caffemodel
rm -rf /modelState/caffe_alexnet_iter_200000.solverstate
echo '['$(date)']:' "Model evaluation complete."