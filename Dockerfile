FROM nimaid/jupyterlab

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="python3 -m pip install --upgrade --no-cache-dir --retries 10 --timeout 60" && \
    GIT_CLONE="git clone --depth 10" && \
    
    apt-get update && \
    
    # Install imagecluster library
    $APT_INSTALL python3-dev && \
    $PIP_INSTALL git+git://github.com/elcorto/imagecluster.git && \
    
    # Clean up
    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*

# Pre-download the model weights
RUN mkdir -p /root/.keras/models/ && \
    cd /root/.keras/models/ && \
    wget https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_tf_dim_ordering_tf_kernels.h5

# Copy wrapper script
COPY imagecluster.py /usr/local/bin/imagecluster
RUN chmod +x /usr/local/bin/imagecluster