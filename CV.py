import cv2 #pip install opencv-python
from facenet_pytorch import MTCNN #pip install facenet-pytorch


class FaceDetector:
    def __init__(self, video_path):
        # Load the MTCNN detector
        self.mtcnn = MTCNN()

        # Open the video file
        self.cap = cv2.VideoCapture(video_path)

    def detect_faces(self):
        while True:
            # Read the frame
            _, img = self.cap.read()

            # Break the loop if the video has ended
            if img is None:
                break

            # Convert to RGB (MTCNN uses RGB format)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Detect faces using MTCNN
            boxes, _ = self.mtcnn.detect(rgb_img)

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
        self.cap.release()

        # Destroy all OpenCV windows
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Create an instance of the FaceDetector class with the video file path
    face_detector = FaceDetector('1.mp4')
    # Call the detect_faces method to start face detection
    face_detector.detect_faces()
