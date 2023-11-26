import cv2 #pip install opencv-python
from facenet_pytorch import MTCNN #pip install facenet-pytorch

# Load the MTCNN detector
mtcnn = MTCNN()

# To use a video file as input
cap = cv2.VideoCapture('1.mp4')

while True:
    # Read the frame
    _, img = cap.read()

    # Convert to RGB (MTCNN uses RGB format)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces using MTCNN
    boxes, _ = mtcnn.detect(rgb_img)

    # Draw the rectangle around each detected face
    if boxes is not None:
        for box in boxes:
            cv2.rectangle(img, tuple(map(int, box[:2])), tuple(map(int, box[2:])), (255, 0, 0), 2)

    # Display the result
    cv2.imshow('Face Detection', img)

    # Break the loop if the 'Esc' key is pressed
    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break

# Release the VideoCapture object
cap.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
