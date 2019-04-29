#!/bin/bash
# Convert a keras model to EVERYTHING

if [ "$1" == "" ]; then
    echo "You must pass at least 1 param - where's that model?"
    exit 1
fi

# Keras to TensorflowJS
./keras_to_tfjs.sh $1 $2
# Keras to Tensorflow
./keras_to_tf.sh $1 $2
