#!/usr/bin/env sh

###################################################
########## RUN THE PREPROCESSING ROUTINE ##########
###################################################

# The following volumes are mounted when the preprocessing container is run:
# - /trainingData (RO)
# - /metadata (RO)
# - /preprocessedData (RW)
# furthermore, /metadata contains the following files:
# - /metadata/exams_metadata.tsv
# - /metadata/images_crosswalk.tsv
# - /metadata/subjects_metadata.tsv (deprecated)

# Display host specs
echo $(nproc) CPUs available.

# Create sub directories
mkdir -p /preprocessedData/data
echo '['$(date)']:' "/preprocessedData/data created."
mkdir -p /preprocessedData/labels
echo '['$(date)']:' "/preprocessedData/labels created."
mkdir -p /preprocessedData/lmdbs
echo '['$(date)']:' "/preprocessedData/lmdbs created."

# generate:
# - labels.txt
# - parallel_commands_preprocess.txt
# - parallel_commands_resize.txt
# - parallel_commands_augment.txt
echo '['$(date)']:' "Generating labels.txt..."
python generate_labels.py
echo '['$(date)']:' "labels.txt generated."

# parallel convert DICOMs to PNGs & apply preprocessing
echo '['$(date)']:' "Converting DICOMs to PNGs..."
sudo ln /dev/null /dev/raw1394
parallel < /preprocessedData/labels/parallel_commands_preprocess.txt
echo '['$(date)']:' "DICOM to PNG conversion done."

# parallel resize preprocessed PNGs
echo '['$(date)']:' "Resizing images..."
parallel < /preprocessedData/labels/parallel_commands_resize.txt
echo '['$(date)']:' "Resizing done."

# parallel augment resized preprocessed PNGs
echo '['$(date)']:' "Augmenting dataset..."
parallel < /preprocessedData/labels/parallel_commands_augment.txt
echo '['$(date)']:' "Dataset augmented."

# Generate train_lmdb
echo '['$(date)']:' "Generating train_lmdb..."
./create_lmdb.sh
echo '['$(date)']:' "train_lmdb generated."

# Generate training mean_image file
echo '['$(date)']:' "Creating mean image..."
./create_mean_image.sh
echo '['$(date)']:' "Mean image created."