#!/bin/bash

while getopts ":i:" opt; do
    case $opt in
        i)
            INPUT_PATH=$OPTARG
            ;;
    esac
done

if [ -z "${INPUT_PATH}" ]; then
    echo "Missing input path for -i argument"
    exit 1
fi

WORKDIR=/home/dfgvi 

docker run \
    -it \
    --rm \
    --gpus=all \
    --shm-size 8G \
    -v "${INPUT_PATH}":"${WORKDIR}/content" \
    dfgvi
