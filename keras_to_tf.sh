#!/bin/bash
# Convert a keras model to Tensorflow

if [ "$1" == "" ]; then
    echo "You must pass at least 1 param - where's that model?"
    exit 1
fi

# No name passed? Just use "model"
NAME=${2:-model}
RESULT_DIR="TF_${NAME}"
K2TF="/Users/gantman/Documents/Projects/ml/keras_to_tensorflow/keras_to_tensorflow.py"

mkdir $RESULT_DIR
# convert to Tensorflow (expects python3 and keras_to_tensorflow)
# https://github.com/amir-abdi/keras_to_tensorflow
python3 $K2TF --input_model=$1 --output_model=./$RESULT_DIR/$NAME.pb
# Quantized version
python3 $K2TF quantize=true --input_model=$1 --output_model=./$RESULT_DIR/quant_$NAME.pb
