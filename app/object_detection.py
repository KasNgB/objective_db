import cv2
import numpy as np
import matplotlib.pyplot as plt

CASSCADEPATH = '~/workstation/objective_db/datasets/apple_dataset/00002.xml'
IMAGEPATH = '~/workstation/objective_db/test_pictures/apple1.jpg'

image = cv2.imread(IMAGEPATH)
apple_cascade = cv2.CascadeClassifier(CASSCADEPATH)

def detect_apple(img):
    apple_img = img.copy()
    apple_rect = apple_cascade.detectMultiScale(apple_img, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in apple_rect:
        cv2.rectangle(apple_img, (x, y), (w + w, y + h), (255, 255, 255), 10)

    return apple_img

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
