#!/usr/bin/env python3

import cv2
import os
import sys
import yaml
import numpy as np

import base64

# Mine now
from config import Config


face_recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')

subjects={}
subjectToLabel={}

def encode_image(img):

   if img is None:
       return None

   bytes = cv2.imencode('.jpeg', img)[1].tostring()
   return base64.b64encode(bytes).decode('utf-8')


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def detect_face(img, body=None):
    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    if (len(faces) == 0):
        return None, None

    #under the assumption that there will be only one face,
    #extract the face area and draw a rectangle
    (x, y, w, h) = faces[0]
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    if body:
        draw_text(img, body['name'], x, y)
    cv2.imshow('video',img)
    
    #return only the face part of the image
    return img[y:y+w, x:x+h], faces[0]

"""
First try using local OpenCV. If confidence is low (high)
fall back to (from cheap to price):

    1. Kairos
    2. Azure
    3. AWS
"""
def identify_face(face):

    label, confidence = face_recognizer.predict(face)
    if label and confidence < 40:
        return subjects[label]
    return None


def __get_subjects_metadata(directory='known_faces'):
    mf = os.path.join(directory, 'metadata.yaml')
    if not os.path.exists(mf):
        return []

    with open(mf, 'r') as m:
        known_metadata = yaml.load(m)
    print(known_metadata)
    return known_metadata


def __get_label(subject):
    if subjectToLabel.get(subject):
        return subjectToLabel.get(subject)

    label = len(subjects) + 1
    subjectToLabel[subject] = label
    return label


def get_known_subjects(directory='known_faces'):
    faces = []
    labels = []

    if os.path.exists('traindata.yml'):
        face_recognizer.load('traindata.yml')

    current_known_people = __get_subjects_metadata()
    if current_known_people is None:
        return None

    for sb in current_known_people:
        print("PROCESSING Images by %s" % (sb['name']))
        for image_path in sb['files']:
            image_path = "%s/%s" % (directory, image_path)
            print('Learning %s' % image_path)
            if not os.path.exists(image_path):
                continue
            image = cv2.imread(image_path)
            if image is None:
                continue

            try:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            except:
                continue

            try:
                detected_faces = faceCascade.detectMultiScale(gray)
            except:
                continue
            for (x, y, w, h) in detected_faces:
                label = __get_label(sb['name'])
                subjects[label] = sb

                faces.append(gray[y:y+h,x:x+w])
                labels.append(label)
    if len(faces) > 0:
        face_recognizer.train(faces, np.array(labels))

    # FIXME: TBD
    return None
    if os.path.exists('training.yml'):
        face_recognizer.update('training.yml', labels)
    else:
        face_recognizer.write('training.yml')


if __name__ == '__main__':
    get_known_subjects()
    cap = cv2.VideoCapture(0)
    cap.set(3,1024) # set Width
    cap.set(4,768) # set Height

    body=None
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #cv2.imshow('frame', frame)
        #cv2.imshow('gray', gray)

        face, rect = detect_face(gray, body)
        if face is not None:
            body = identify_face(face)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
