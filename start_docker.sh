#!/bin/sh
# usage: ./start_docker.sh <GPU number>
docker run -u $(id -u):$(id -g) --rm --runtime=nvidia -it -v /data:/data -e CUDA_VISIBLE_DEVICES=$1 -e USER=$USER -e HOME=/data/$USER -w $PWD burn_severity/latest bash

