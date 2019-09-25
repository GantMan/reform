from tensorflowjs import converters
from keras.models import load_model
from keras import backend as K
import tensorflow as tf
from zipfile import ZipFile
import os


keras_model = r'C:\Users\selvam\Downloads\model.h5' # path of the Keras model file
tfjs_dir = r'C:\Users\selvam\Downloads' # path of the Tensorflow JS directory
tflite_dir = r'C:\Users\selvam\Downloads\model.tflite' # path of the Tensorflow LITE file
tf_dir = r'C:\Users\selvam\Downloads' # path of the Tensorflow directory
tf_file = 'model.pb' # Tensorflow file name

tf.compat.v1.disable_eager_execution()

model = load_model(keras_model)

# Convert Keras to Tensorflow
def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            session, input_graph_def, output_names, freeze_var_names)
        return frozen_graph
      

frozen_graph = freeze_session(K.get_session(), output_names=[out.op.name for out in model.outputs])
tf_pb = tf.train.write_graph(frozen_graph, tf_dir, tf_file, as_text=False)


# Convert Keras to TFLITE
converter = tf.lite.TFLiteConverter.from_keras_model_file(keras_model)
tfmodel = converter.convert()
tflite = open(tflite_dir,"wb").write(tfmodel)

# Convert Keras to Tensorflow JS
# If tensorflow JS library missing the dispatch_keras_h5_to_tfjs_layers_model_conversion function in init.py add the function
tf_js = converters.dispatch_keras_h5_to_tfjs_layers_model_conversion(keras_model, tfjs_dir)

# Zip all the Files
zipObj = ZipFile(tfjs_dir + r'model.zip', 'w')
 
# Add multiple files to the zip
zipObj.write(tfjs_dir + r'\model.tflite')
zipObj.write(tfjs_dir + r'\model.pb')
zipObj.write(tfjs_dir + r'\model.json')
 
# Close the Zip File
zipObj.close()

# Removing the files after Zip
os.remove(tfjs_dir + r'\model.tflite')
os.remove(tfjs_dir + r'\model.pb')
os.remove(tfjs_dir + r'\model.json')


