import numpy as np
import nibabel as nib
from scipy.ndimage import zoom
import tensorflow as tf

def load_preprocess_and_predict(file_path, image_size=(64, 64, 64)):
    img = nib.load(file_path).get_fdata()
    img = zoom(img, (image_size[0] / img.shape[0], image_size[1] / img.shape[1], image_size[2] / img.shape[2]), order=1)
    img = img[..., np.newaxis]
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=0) 
    model = tf.keras.models.load_model('3d-cnn-lstm.keras')
    prediction = model.predict(img)
    class_labels = ['Alzheimers Disease (AD)', 'Cognitive Normal (CN)', 'Mild Cognitive Impairment (MCI)', 'Early Mild Cognitive Impairment (EMCI)']
    predicted_class = np.argmax(prediction, axis=1)
    
    return class_labels[predicted_class[0]]

