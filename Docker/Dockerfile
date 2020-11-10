FROM nvidia/cuda:10.0-devel-ubuntu18.04

##############################################################################
# Versions
##############################################################################
ENV PYTHON_VERSION=3
ENV TENSORFLOW_VERSION=1.15.2
ENV PYTORCH_VERSION=1.2.0
ENV TORCHVISION_VERSION=0.4.0
ENV TENSORBOARDX_VERSION=1.8
ENV CUDNN_VERSION=7.6.0.64-1+cuda10.0
ENV NCCL_VERSION=2.4.7-1+cuda10.0
ENV MXNET_VERSION=1.5.0

##############################################################################
# Installation/Basic Utilities
##############################################################################
RUN apt-get update && \
    apt-get install -y --allow-change-held-packages --no-install-recommends \
    software-properties-common \
    openssh-client openssh-server \
    pdsh curl sudo net-tools \
    vim iputils-ping wget perl \
    libxml-parser-perl \
    libcudnn7=${CUDNN_VERSION} \
    libnccl2=${NCCL_VERSION} \
    libnccl-dev=${NCCL_VERSION} \
    --allow-downgrades

##############################################################################
# Installation Latest Git
##############################################################################
RUN add-apt-repository ppa:git-core/ppa -y && \
    apt-get update && \
    apt-get install -y git && \
    git --version

##############################################################################
# Python and Pip
##############################################################################
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3 python3-dev && \
    rm -f /usr/bin/python && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
        python get-pip.py && \
        rm get-pip.py && \
    pip install --upgrade pip && \
    # Print python an pip version
    python -V && pip -V

##############################################################################
# MXNet
##############################################################################
RUN pip install mxnet-cu100==${MXNET_VERSION}

##############################################################################
# TensorFlow
##############################################################################
RUN pip install tensorflow-gpu==${TENSORFLOW_VERSION}

##############################################################################
# PyTorch
##############################################################################
RUN pip install torch==${PYTORCH_VERSION}
RUN pip install torchvision==${TORCHVISION_VERSION}
RUN pip install tensorboardX==${TENSORBOARDX_VERSION}

##############################################################################
# Temporary Installation Directory
##############################################################################
ENV STAGE_DIR=/tmp
RUN mkdir -p ${STAGE_DIR}

##############################################################################
# Mellanox OFED
##############################################################################
ENV MLNX_OFED_VERSION=4.6-1.0.1.1
RUN apt-get install -y libnuma-dev
RUN cd ${STAGE_DIR} && \
    wget -q -O - http://www.mellanox.com/downloads/ofed/MLNX_OFED-${MLNX_OFED_VERSION}/MLNX_OFED_LINUX-${MLNX_OFED_VERSION}-ubuntu18.04-x86_64.tgz | tar xzf - && \
    cd MLNX_OFED_LINUX-${MLNX_OFED_VERSION}-ubuntu18.04-x86_64 && \
    ./mlnxofedinstall --user-space-only --without-fw-update --all -q && \
    cd ${STAGE_DIR} && \
    rm -rf ${STAGE_DIR}/MLNX_OFED_LINUX-${MLNX_OFED_VERSION}-ubuntu18.04-x86_64*

##############################################################################
# Install Open MPI
##############################################################################
RUN mkdir ${STAGE_DIR}/openmpi && \
    cd ${STAGE_DIR}/openmpi && \
    wget https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-4.0.1.tar.gz && \
    tar zxf openmpi-4.0.1.tar.gz && \
    cd openmpi-4.0.1 && \
    ./configure --enable-orterun-prefix-by-default && \
    make -j $(nproc) all && \
    make install && \
    ldconfig && \
    rm -rf ${STAGE_DIR}/openmpi

##############################################################################
# Ucomment and set SSH Daemon port
###############################################################################
RUN mkdir -p /var/run/sshd
# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config
# SSH Daemon port for DeepSpeed
ENV SSH_PORT=2222
RUN cat /etc/ssh/sshd_config > ${STAGE_DIR}/sshd_config && \
    sed "0,/^#Port 22/s//Port ${SSH_PORT}/" ${STAGE_DIR}/sshd_config > /etc/ssh/sshd_config

##############################################################################
# Common Python Packages
##############################################################################
RUN pip install future typing
RUN pip install numpy \
                scipy \
                h5py \
                azureml-defaults \
                tqdm \
                scikit-learn \
                pytest \
                boto3 \
                filelock \
                tokenizers \
                requests \
                regex \
                mpi4py \
                sentencepiece \
                sacremoses \
                spacy \
                nltk \
                pyrouge \
                py-rouge \
                seqeval
RUN python -m spacy download en
RUN python -m nltk.downloader punkt

RUN pip install transformers==2.4.1
RUN pip install tokenizers==0.8.1

##############################################################################
# Set default shell to /bin/bash
##############################################################################
SHELL ["/bin/bash", "-cu"]
