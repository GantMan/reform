#!/bin/bash
# Convert file to a zip

if [ "$1" == "" ]; then
    echo "First parameter is the path"
    exit 1
fi

if [ "$2" == "" ]; then
    echo "Second parameter is the file"
    exit 1
fi

# No name passed? Just use "result"
NAME=${3:-result}

# Regular
zip $1/results/$NAME.zip $1/$2
