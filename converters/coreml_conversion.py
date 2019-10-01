from coremltools.converters import caffe, keras sklearn, xgboost

def caffe_model(caffe_model_file_path, caffe_prototxt_file_path):
    # Sometimes, critical information in the Caffe converter is missing from the .caffemodel file. 
    #This information is present in the deploy.prototxt file. 
    #You can provide us with both files in the conversion process.
 
    if caffe_model_file_path == True and caffe_prototxt_file_path == True:
        #caffe to coreml
        caffe_to_coreml = caffe.convert(caffe_input, caffe_prototxt)
        caffe_to_coreml = caffe_to_coreml.save('./path/to/save/caffe_to_coreml.mlmodel')
    elif caffe_model == True and caffe_prototxt == False:
        caffe_to_coreml = caffe.convert(caffe_input)
        caffe_to_coreml = caffe_to_coreml.save('./path/to/save/caffe_to_coreml.mlmodel')     
    return caffe_to_coreml


def keras_model (keras_file_path):
    keras_to_coreml = keras.convert(keras_file_path)
    keras_to_coreml = keras_to_coreml.save('./path/to/save/keras_to_coreml.mlmodel') 
    return keras_to_coreml
    
def sklearn_model (sklearn_file_path, input_feaure, output_feature): 
    sk_to_coreml = sklearn.convert(sklearn_file_path, input_feaure, output_feature)
    sk_to_coreml = sk_to_coreml.save('./path/to/save/sk_to_coreml.mlmodel')
    return sk_to_coreml

def xg_model (xg_file_path):
    xg_to_coreml = xgboost.convert(xg_file_path)
    xg_to_coreml = xg_to_coreml.save('./path/to/save/sk_to_coreml.mlmodel')
    return xg_to_coreml
