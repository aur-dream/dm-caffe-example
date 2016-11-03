########################################
########## START DEPENDENCIES ##########
########################################

FROM nvidia/caffe

RUN apt-get update && apt-get install -y \
  python-dev \
  python-pip

# Check how to test caffe - RUN make test
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
RUN apt-get install libdc1394-22-dev libdc1394-22 libdc1394-utils -y

######################################
########## END DEPENDENCIES ##########
######################################

###################################################
########## PREPARE PREPROCESSING ROUTINE ##########
###################################################

# Copy files
RUN echo "Copying files..."
COPY train.sh /train.sh
COPY bashrc /.bashrc
COPY caffe-ld-so.conf /caffe-ld-so.conf
COPY test_solver.prototxt /test_solver.prototxt
COPY full_solver.prototxt /full_solver.prototxt
COPY train.prototxt /train.prototxt
COPY deploy.prototxt /deploy.prototxt
COPY generate_parallel_commands.py /generate_parallel_commands.py
COPY preprocess_dm_images.py /preprocess_dm_images.py
COPY test_model.py /test_model.py
#COPY caffe_googlenet_iter_200000.caffemodel /caffe_googlenet_iter_200000.caffemodel
RUN echo "Files copied."

# Set permissions so server can execute within Docker container
RUN echo "Setting file permissions..."
RUN chmod 777 /train.sh
RUN chmod 777 /.bashrc
RUN chmod 777 /caffe-ld-so.conf
RUN chmod 777 /test_solver.prototxt
RUN chmod 777 /full_solver.prototxt
RUN chmod 777 /train.prototxt
RUN chmod 777 /deploy.prototxt
RUN chmod 777 /generate_parallel_commands.py
RUN chmod 777 /preprocess_dm_images.py
RUN chmod 777 /test_model.py
#RUN chmod 777 /caffe_googlenet_iter_200000.caffemodel
RUN echo "File permissions set."

