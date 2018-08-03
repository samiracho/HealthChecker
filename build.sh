#!/bin/bash

if [ -z "$HK_NOTIFY_TOKEN" ]; then
    echo "You need to set the env variable $HK_NOTIFY_TOKEN"
    echo "Execute: export HK_NOTIFY_TOKEN=auth_token"
    exit 1
fi

echo "Pass tests"
python3 -m unittest discover -p 'test*.py'

if [ $? -eq 0 ]; then
    echo "Build docker image"
    docker build -t healthchecker  --build-arg HK_NOTIFY_TOKEN=$HK_NOTIFY_TOKEN .
else
    echo "Tests failed. Aborting"
fi