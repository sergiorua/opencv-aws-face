import cv2
import time
import os

current_millis = lambda: int(round(time.time() * 1000))
storage_location = 'captures'

def save_image(filename, file):
    cv2.imwrite(os.path.join(storage_location, filename), file)

def capture_id():
    return '{}.bmp'.format(current_millis())

def capture():

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Camera", cv2.WINDOW_FULLSCREEN)
    image = None
    image_id = None

    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 32:
            image_id = capture_id()
            image = frame
            save_image(image_id, image)
            continue
        elif k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return image_id, image

if __name__ == '__main__':
    if not os.path.exists(storage_location):
        os.mkdir(storage_location)
    capture()