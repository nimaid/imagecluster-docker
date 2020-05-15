@echo off
docker run -it -v %~dp0\data:/root/data -p 8888:8888 nimaid/imagecluster
