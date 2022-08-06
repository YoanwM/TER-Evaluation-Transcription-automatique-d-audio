# YOLO object detection
import cv2 as cv
import numpy as np
import time
import pathlib
import os
import argparse



# Argument parsing

parser = argparse.ArgumentParser()
parser.add_argument('--title', nargs=1, help='title of the video to process', required=True)
parser.add_argument('--frame_drop', nargs=1, help='Images every frame drop will be processed', required=False, default=50)
parser.add_argument('--confidence_min', nargs=1, help='Images every frame drop will be processed', required=False, default=0.5, type=float)
args = parser.parse_args()
title = args.title[0]
frame_drop = args.frame_drop
confidence_min = args.confidence_min[0]

# Remove files and recreates directories
os.system("rm -rf ./"+title)
os.mkdir(title)
os.mkdir("./"+title+"/Images")
os.mkdir("./"+title+"/Results")

# Making different path

path = pathlib.Path().parent.absolute()
video_path = str(path) + "/../videos/" + title + "/" + title + ".mp4"
config_path = str(path) + "/yolov3.cfg"
classes_path = str(path) + "/yolov3.txt"
weights_path = str(path) + "/yolov3.weights"


# Creating the images

cap = cv.VideoCapture(video_path)
i = 0
nb_img = 0
while True:

    ret, image = cap.read()
    if ret:
        if i == 0:
            cv.imwrite(title + "/Images/" + title + str(nb_img) + ".jpg", image)
            nb_img += 1
    else:
        break
    i = (i + 1) % frame_drop
print("All images have been extracted")


# Processing object detection

WHITE = (255, 255, 255)
img = None
img0 = None
outputs = None

# Load names of classes and get random colors
classes = open('coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

# Give the configuration and weight files for the model and load the network.
net = cv.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# determine the output layer
ln = net.getLayerNames()
print(net.getUnconnectedOutLayers())
ln = [ln[i[0] - 1] for i in [net.getUnconnectedOutLayers()]]


def load_image(path,num_img):
    global img, img0, outputs, ln

    img0 = cv.imread(path)
    img = img0.copy()

    blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    net.setInput(blob)
    t0 = time.time()
    outputs = net.forward(ln)
    t = time.time() - t0

    # combine the 3 output groups into 1 (10647, 85)
    # large objects (507, 85)
    # medium objects (2028, 85)
    # small objects (8112, 85)
    outputs = np.vstack(outputs)

    post_process(img, outputs, confidence_min, num_img)
    cv.imshow('window', img)
    cv.displayOverlay('window', f'forward propagation time={t:.3}')
    cv.imwrite(title + "/Results/" + title + str(num_img) + ".jpg", img)
    #cv.waitKey(0)


def post_process(img, outputs, conf, num_img):
    H, W = img.shape[:2]

    boxes = []
    confidences = []
    classIDs = []

    file = open("./"+title+"/"+title+".txt","a")


    for output in outputs:
        scores = output[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > conf:
            x, y, w, h = output[:4] * np.array([W, H, W, H])
            p0 = int(x - w // 2), int(y - h // 2)
            p1 = int(x + w // 2), int(y + h // 2)
            boxes.append([*p0, int(w), int(h)])
            confidences.append(float(confidence))
            classIDs.append(classID)
            # cv.rectangle(img, p0, p1, WHITE, 1)

    indices = cv.dnn.NMSBoxes(boxes, confidences, conf, conf - 0.1)
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in colors[classIDs[i]]]
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            w = str(num_img) + " " + classes[classIDs[i]] + " " + str(confidences[i]) + "\n"
            file.write(w)
            text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
            cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, confidence_min, color, 1)
    file.close()

def trackbar(x):
    global img
    conf = x / 100
    img = img0.copy()
    post_process(img, outputs, confidence_min, 0)
    cv.displayOverlay('window', f'confidence level={conf}')
    cv.imshow('window', img)

def process_images(nb_img):
    for i in range (nb_img) :
        load_image(title + "/Images/" + title + str(i)+ ".jpg",i)

cv.namedWindow('window')
cv.createTrackbar('confidence', 'window', 50, 100, trackbar)
process_images(nb_img)
cv.destroyAllWindows()