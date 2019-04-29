#!/bin/bash
# Convert a keras model to TFJS

if [ "$1" == "" ]; then
    echo "You must pass at least 1 param - where's that model?"
    exit 1
fi

# No name passed? Just use "model"
NAME=${2:-model}
RESULT_DIR="TFJS_${NAME}"

mkdir $RESULT_DIR
# Regular
tensorflowjs_converter --input_format keras $1 ./$RESULT_DIR/tfjs_$NAME
zip ./$RESULT_DIR/tfjs_$NAME.zip ./$RESULT_DIR/tfjs_$NAME/
# Quantized
tensorflowjs_converter --quantization_bytes 1 --input_format keras $1 ./$RESULT_DIR/tfjs_quant_$NAME
zip ./$RESULT_DIR/tfjs_min_$NAME_min.zip ./$RESULT_DIR/tfjs_quant_$NAME/

