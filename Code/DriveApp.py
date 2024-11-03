import numpy as np
import cv2
from keras.models import load_model
import opencv_jupyter_ui as jcv2
model = load_model('/content/Autopilot.h5')

def keras_predict(model, image):
    processed = keras_process_image(image)
    steering_angle = float(model.predict(processed, batch_size=1))
    steering_angle = steering_angle * 100
    return steering_angle


def keras_process_image(img):
    image_x = 40
    image_y = 40
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img


steer = cv2.imread('/content/Resources/steering_wheel_image.jpg', 0)
rows, cols = steer.shape
smoothed_angle = 0

cap = cv2.VideoCapture('/content/Resources/run.mp4')
while (cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.resize((cv2.cvtColor(frame, cv2.COLOR_RGB2HSV))[:, :, 1], (40, 40))
    steering_angle = keras_predict(model, gray)
    print(steering_angle)
    jcv2.imshow('frame', cv2.resize(frame, (500, 300), interpolation=cv2.INTER_AREA))
    smoothed_angle += 0.2 * pow(abs((steering_angle - smoothed_angle)), 2.0 / 3.0) * (
        steering_angle - smoothed_angle) / abs(
        steering_angle - smoothed_angle)
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -smoothed_angle, 1)
    dst = cv2.warpAffine(steer, M, (cols, rows))
    dst_bgr = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR) 
    jcv2.imshow("steering wheel", dst_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()