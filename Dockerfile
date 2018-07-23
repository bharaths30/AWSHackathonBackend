# our base image
FROM ubuntu:16.04

# Install python and pip

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libhdf5-serial-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python \
        python-dev \
        rsync \
        software-properties-common \
        unzip \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

 RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip --no-cache-dir install \
        Pillow \
        h5py \
        ipykernel \
        jupyter \
        matplotlib \
        numpy \
        pandas \
        scipy \
        sklearn \
        && \
    python -m ipykernel.kernelspec

#RUN pip --no-cache-dir install \
#    http://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.0.0-cp27-none-linux_x86_64.whl

# install Python modules needed by the Python app

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app/
RUN mkdir /usr/src/app/images
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

RUN pip install tensorflow --ignore-installed six

# copy files required for the app to run

COPY classify_image.py /usr/src/app/
COPY flask_app.py /usr/src/app/app.py
#COPY templates/index.html /usr/src/app/templates/

COPY dnn_classifier.py /usr/src/app/
COPY model/* /usr/src/app/model/

# tell the port number the container should expose
#EXPOSE 5000

# run the application
CMD ["python", "/usr/src/app/app.py"]
