# -*- encoding:utf-8 -*-

import os
import random
import string
import numpy as np
import cv2
from werkzeug.utils import secure_filename

cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
allow_extends = set(['png','jpeg','jpg','gif'])
digit = 8

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in allow_extends

def image_save(img):

  if img and allowed_file(img.filename):

    ImgName = img.filename
    img = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
    image_gray = cv2.cvtColor(img, cv2.cv.CV_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
    if len(facerect) is 0:
      result = ["None Face",False]

    else:

      for clip in facerect:
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(digit)])
        dst = img[clip[1]-(clip[1]/3):clip[1]+clip[3]+((clip[1]+clip[3])/3),clip[0]:clip[0]+clip[2]]
        cv2.imwrite('./static/image/guest/'+secure_filename(random_str+ImgName),dst)
        result = ['./static/image/guest/'+secure_filename(random_str+ImgName),True]

  else:
    result = ["no match allow",False]

  return result
