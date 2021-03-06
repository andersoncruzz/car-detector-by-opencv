# import the necessary packages
import numpy as np
import cv2
import os


VIDEO_INPUT = "video.mp4"
OUTPUT_DIRECTORY = "output"

if os.path.exists(OUTPUT_DIRECTORY) == False:
    os.makedirs(OUTPUT_DIRECTORY)


prototxt = "models/deploy.prototxt.txt"
model = "models/MobileNetSSD_deploy.caffemodel"
CONST_CONFIDENCE = 0.1

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# force color to car be red
COLORS[7] = (0, 0, 255)

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# (note: normalization is done via the authors of the MobileNet SSD
# implementation)

video = cv2.VideoCapture(os.path.join("input", VIDEO_INPUT))

j = 1

while(video.isOpened()):
    print("j: ", j)
    ret, frame = video.read()

    if ret == False:
        break

    print("ret: ", ret)
    (h, w) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.014843,
        (300, 300), 0.0) #1050



    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    flag = False

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]



        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > CONST_CONFIDENCE:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])

            if CLASSES[idx] == "car":
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # display the prediction
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                flag = True
    if flag:
        # show the output image
        cv2.imwrite(os.path.join(OUTPUT_DIRECTORY, VIDEO_INPUT.split(".")[0] + "_" + str(j) + "_out.png"), frame)
    j += 1

video.release()
