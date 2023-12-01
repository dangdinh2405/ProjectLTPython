import os
import speech_recognition as sr
import cv2
from PIL import Image, ImageTk
from facenet_pytorch import MTCNN
import tkinter as tk
from tkinter import filedialog

class FaceDetector:
    def __init__(self, root):
        self.mtcnn = MTCNN()
        self.root = root
        self.cap = None

        self.frames_to_cut = 5  # Số lượng frame cần cắt
        self.detected_frames = []  # Danh sách các frame đã nhận diện
        self.frame_count = 0

        self.top_level_window = tk.Toplevel(self.root)
        self.top_level_window.title("Face Detection")
        self.top_level_window.geometry("300x100")
        self.output_folder = "./"

        self.recognizer = sr.Recognizer()

    def voice_command(self, command):
        if "input" in command:
            self.choose_file()
        elif "output" in command:
            self.imageDetect()

    def listen_voice_command(self):
        with sr.Microphone() as source:
            print("Say something...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=3)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            self.voice_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.detect_faces()

    def imageDetect(self):

        for i, frame in enumerate(self.detected_frames):
            cv2.imshow(f'Detected Face {i + 1}', frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if self.output_folder:
                save_path = os.path.join(self.output_folder, f"detected_face_{i + 1}.png")
                pil_img.save(save_path)

    def detect_faces(self):
        while True:
            _, img = self.cap.read()
            if img is None:
                break

            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes, _ = self.mtcnn.detect(rgb_img)

            if boxes is not None:
                for box in boxes:
                    cv2.rectangle(img, tuple(map(int, box[:2])), tuple(map(int, box[2:])), (255, 0, 0), 2)

                if self.frame_count != self.frames_to_cut:
                    self.detected_frames.append(img.copy())
                    self.frame_count += 1

            cv2.imshow('Face Detection', img)

            key = cv2.waitKey(30) & 0xFF
            if key == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def run_gui(self):
        label = tk.Label(self.top_level_window, text="Choose a video file:")
        label.pack(pady=10)

        tk.Button(self.top_level_window, text="Close", command=self.on_close_callback).place(x=230, y=50)

        button = tk.Button(self.top_level_window, text="Input", command=self.choose_file)
        button.place(x=50, y=50)

        button = tk.Button(self.top_level_window, text="Output", command=self.imageDetect)
        button.place(x=100, y=50)

        button = tk.Button(self.top_level_window, text="Voice", command=self.listen_voice_command)
        button.place(x=230, y=7)

        self.top_level_window.mainloop()

    def on_close_callback(self):
        # Close the top-level window
        self.top_level_window.destroy()


if __name__ == "__main__":
    face_detector = FaceDetector()
    face_detector.run_gui()
