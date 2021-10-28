import io
import os
from flask import Flask, render_template, redirect, url_for, Response, request, session
import urllib
import cv2
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import imutils
import easyocr
from PIL import Image
from flask import Flask , render_template  , request , send_file

app = Flask(__name__)
BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')

def number_plate(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

    bfilter=cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

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
    plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y)) #top left corner
    (x2, y2) = (np.max(x), np.max(y))  #bottom right corner
    cropped_image = gray[x1:x2+1, y1:y2+1] #buffer +1

    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    text = result[0][-2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
    fig = plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    return fig
    
@app.route('/')
def home():
        return render_template("index.html")

@app.route('/plate.png' , methods = ['GET' , 'POST'])
def plate_png():
	
    file = request.files.get('image')
    print("file = ", file)
    # Read the image via file.stream
    img = Image.open(file.stream).convert('RGB')
    #img.show()

    #return jsonify({'msg': 'success', 'size': [img.width, img.height]})

    image = np.array(img)
    image = cv2.resize(image, (600, 360))
    # cv2.imshow("Output ANPR", image)
    # cv2.waitKey(0)

    fig = number_plate(image)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
