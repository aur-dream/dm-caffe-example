########################################
########## START DEPENDENCIES ##########
########################################

FROM nvidia/caffe
#FROM tschaffter/caffe-gpu

RUN apt-get update && apt-get install -y \
  python-dev \
  python-pip

# Check how to test caffe - RUN make test #
RUN pip install pydicom
RUN apt-get build-dep -y python-matplotlib
RUN pip install synapseclient
RUN pip install lmdb
RUN apt-get install python-opencv
# needed to avoid issues with cv2
RUN ln /dev/null /dev/raw1394
RUN pip install sklearn

# GNU parallel and imagemagick for image processing boost (and OpenCV)
RUN apt-get install imagemagick php5-imagick -y
RUN apt-get install parallel -y
RUN apt-get install gnome-session-fallback -y
RUN apt-get install python-opencv -y

######################################
########## END DEPENDENCIES ##########
######################################

###################################################
########## PREPARE PREPROCESSING ROUTINE ##########
###################################################

# Copy files
RUN echo "Copying files..."
COPY preprocess_dm_images.py /preprocess_dm_images.py
COPY generate_labels.py /generate_labels.py
COPY create_lmdb.sh /create_lmdb.sh
COPY create_mean_image.sh /create_mean_image.sh
COPY preprocess.sh /preprocess.sh
COPY bashrc /.bashrc
COPY caffe-ld-so.conf /caffe-ld-so.conf
COPY rotate_image.py /rotate_image.py
RUN echo "Files copied."

# Set permissions so server can execute within Docker container
RUN echo "Setting file permissions..."
RUN chmod 777 /preprocess_dm_images.py
RUN chmod 777 /generate_labels.py
RUN chmod 777 /create_lmdb.sh
RUN chmod 777 /create_mean_image.sh
RUN chmod 777 /preprocess.sh
RUN chmod 777 /.bashrc
RUN chmod 777 /caffe-ld-so.conf
RUN chmod 777 /rotate_image.py
RUN echo "File permissions set."

