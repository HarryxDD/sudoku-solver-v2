import cv2
import numpy as np
import os
import tensorflow.keras.models as tf

# load_model
model = tf.load_model('model/model.h5')


# functions
def img_handler(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5,5), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, 1, 1, 11, 2)
    
    return img_thresh


def rect_contours(contours):
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            biggest = approx

    return biggest


def perspective_trans(shape, img, w, h):
    pts1 = np.float32(shape)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warp = cv2.warpPerspective(img, matrix, (w, h))
    img_warp = cv2.cvtColor(img_warp, cv2.COLOR_BGR2GRAY)
    return img_warp


def split_img(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes


def four_points(shape):
    biggest = np.zeros((4, 1, 2), dtype=np.int32)
    add = shape.sum(1)
    biggest[0] = shape[np.argmin(add)]
    biggest[3] = shape[np.argmax(add)]
    middle = np.diff(shape, axis=1)
    biggest[1] = shape[np.argmin(middle)]
    biggest[2] = shape[np.argmax(middle)]

    return biggest


def ques_digit(boxes):
    ques = []
    for image in boxes:
        im = np.asarray(image)
        im = im[4:im.shape[0] - 4, 4:im.shape[1] -4]
        im = cv2.resize(im, (28, 28))
        im = im / 255
        im = im.reshape(1, 28, 28, 1)
        # get predition
        predictions = model.predict(im)
        class_idx = np.argmax(predictions, axis=1)
        probabilityValue = np.amax(predictions)
        # save the result
        if probabilityValue > 0.8:
            ques.append(class_idx[0])
        else:
            ques.append(0)
            
    ques = np.asarray(ques)

    return ques


def ans_digit(img, number, color=(0, 255, 0)):
    width = int(img.shape[1]/9)
    height = int(img.shape[0]/9)
    for x in range(0,9):
        for y in range(0,9):
            if number[(y*9)+x] != 0:
                cv2.putText(img, str(number[(y*9)+x]), (x*width+width-40, int((0.7+y)*height)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, color, 2, cv2.LINE_AA)

    return img


##################################################