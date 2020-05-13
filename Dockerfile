FROM nimaid/cuda-jupyterlab

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="python3 -m pip install --upgrade --no-cache-dir --retries 10 --timeout 60" && \
    GIT_CLONE="git clone --depth 10" && \
    
    apt-get update && \
    
    # Install imagecluster library with GPU support (hopefully, I don't actually know what I'm doing)
    $APT_INSTALL python3-dev && \
    cd /root/ && \
    $GIT_CLONE https://github.com/elcorto/imagecluster.git && \
    cd imagecluster/ && \
    sed -i '/tensorflow/c\tensorflow-gpu' requirements.txt && \
    pip3 install -e . && \
    
    # Clean up
    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*
