import io
import os
from flask import Flask, render_template, redirect, url_for, Response, request, session
import cv2
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import imutils
import easyocr
from flask import Flask , render_template  , request , send_file

app = Flask(__name__,template_folder='templates')
BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')

def number_plate(path,filename):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bfilter=cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection

    #contour detection - shapes basically
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#approximate the contour
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #top 10 contours

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)#allows to approximate the polygon from our contour, rough sides
        if len(approx) == 4:   #if the approximation has 4 keypoints -- number plate location
            location = approx
            break
    location

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y)) #top left corner
    (x2, y2) = (np.max(x), np.max(y))  #bottom right corner
    cropped_image = gray[x1:x2+1, y1:y2+1] #buffer +1


    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    text = result[0][-2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
    return text
    

@app.route('/')
def home():
        return render_template("index.html")
    
@app.route('/success' , methods = ['GET' , 'POST'])
def success():
  if request.method == 'POST':
    upload_file = request.files['file']
    filename = upload_file.filename
    path_save = os.path.join(UPLOAD_PATH,filename)
    upload_file.save(path_save)
    text = number_plate(path_save,filename)

    return render_template('data.html',text=text)
  return render_template('index.html',upload=False)

if __name__ == "__main__":
    app.run(debug=True)
