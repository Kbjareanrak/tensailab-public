# prepare OpenCV, pyzbar, datetime, csv and winsound libraries
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import csv
import winsound

# source preparation: image file, video file, camera
cap = cv2.VideoCapture(0)
Barcodes = []
with open('products.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'tag']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

while True:
    # read image
    ret,img = cap.read()
    # pre-process image
    img = cv2.flip(img, flipCode=1)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # extract QR code from image
    barcodes = decode(gray_img)
    for barcode in barcodes:
        tag = barcode.data.decode('utf8')
        if tag not in Barcodes: 
            Barcodes.append(tag)
            t = datetime.now()
            print(str(t) + ' : ' + tag)
            with open('products.csv', 'a', newline='') as csvfile:
                fieldnames = ['timestamp', 'tag']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'timestamp': str(t), 'tag': tag})
            winsound.Beep(2000, 200)
    # preview image and update GUI
    cv2.imshow('Preview', img)
    if cv2.waitKey(10) == ord('q'):
        break
cap.release()