@echo off
docker run -it -v %~dp0\data:/root/data nimaid/imagecluster imagecluster %*
