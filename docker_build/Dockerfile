FROM ubuntu

# Install requirements
RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="python3 -m pip install --upgrade --no-cache-dir --retries 10 --timeout 60" && \
    GIT_CLONE="git clone --depth 10" && \
    
    apt-get update && \
    
    # Install imagecluster library
    $APT_INSTALL python3 python3-dev python3-pip python3-setuptools git wget && \
    $PIP_INSTALL git+git://github.com/elcorto/imagecluster.git && \
    
    # Pre-download the model weights
    mkdir -p /root/.keras/models/ && \
    cd /root/.keras/models/ && \
    wget https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels.h5 && \
    
    # Uninstall unneeded packages
    apt-get purge -y python3-pip python3-setuptools git wget && \
    
    # Clean up
    ldconfig && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*

# Copy wrapper script
COPY imagecluster.py /usr/local/bin/imagecluster
RUN chmod +x /usr/local/bin/imagecluster

ENV SHELL bash
WORKDIR /root
CMD ["imagecluster", "--help"]