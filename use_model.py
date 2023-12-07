import tensorflow as tf
import numpy as np
import mss
import pydirectinput as pdi
import time

model = tf.keras.models.load_model('modelmain.h5')


game_area = {"left": 0, "top": 270, "width": 970, "height": 200}

class_labels = {  0 : 'up', 1 : 'up&left', 2: 'up&right'}  # Map class indices to labels


def read_screen():
    with mss.mss() as sct:
        # Capture the screen at the specified game area
        screencap = sct.grab(game_area)
        screencap_np = np.array(screencap)

    # Discard the alpha channel and convert to RGB
    screencap_rgb = screencap_np[:, :, :3]

    # Resize to match the input size of the ResNet50 model (224x224)
    screencap_resized = tf.image.resize(screencap_rgb, (224, 224))

    # Add a batch dimension to the input data
    return np.expand_dims(screencap_resized, axis=0)



if __name__ == "__main__":
    previous_prediction = None
    while True:
        prediction_probabilities = model.predict(read_screen())
        predicted_class_index = np.argmax(prediction_probabilities)
        predicted_class_label = class_labels[predicted_class_index]
        
        if predicted_class_label:
            if '&' in predicted_class_label:
                parts = predicted_class_label.split('&')
                pdi.keyDown(parts[1])
                time.sleep(0.1)
                pdi.keyUp(parts[1])
                pdi.keyDown(parts[0])
                pdi.keyUp(parts[0])
            else:
                pdi.keyDown(predicted_class_label)
                time.sleep(0.1)
                pdi.keyUp(predicted_class_label)
        
        print("Predicted Label:", predicted_class_label)
    