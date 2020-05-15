@echo off
docker run -it --rm -v %~dp0\data:/root/data nimaid/imagecluster imagecluster %*
