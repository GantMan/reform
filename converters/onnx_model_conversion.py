import coremltools
import keras2onnx
from onnxmltools.convert import convert_coreml, convert_keras, convert_sklearn
import onnxmltools
from keras.models import load_model
import pickle

# Keras to onnx
def keras_model(keras_file_path):
    keras_load_model = load_model(keras_file_path)
    keras2onnx = convert_keras(keras_load_model)
    # Save as protobuf
    keras2onnx = onnxmltools.utils.save_model(keras2onnx, '.path/to/save/onnx/model.onnx')
    return keras2onnx

# Coreml to onnx
def coreml_model(coreml_file_path):
    coreml_load_model = coremltools.utils.load_spec('example.mlmodel')
    coreml2onnx = onnxmltools.convert_coreml(coreml_load_model, 'Example Model')
    # Save as protobuf
    coreml2onnx = onnxmltools.utils.save_model(coreml2onnx, '.path/to/save/onnx/model.onnx')
    return coreml2onnx

# sklearn to onnx

def sk_model(sk_file_path):
    sk_load_model = pickle.load(sk_file_path)
    sk2onnx = onnxmltools.convert_sklearn(sk_load_model)
    # Save as protobuf
    sk2onnx = onnxmltools.utils.save_model(sk2onnx, '.path/to/save/onnx/model.onnx')
    return coreml2onnx
