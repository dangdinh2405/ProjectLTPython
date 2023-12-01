import tkinter as tk
from threading import Thread
from tkinter import Canvas
from PIL import Image, ImageTk
import CarRacing
import CV
import EDA


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Đồ án cuối kỳ")
        master.geometry("1000x500")

        # Tạo ba nút
        self.button1 = tk.Button(self.master, text="Face Detection", command=self.FaceDetection, width=11, height=2)
        self.button2 = tk.Button(self.master, text="EDA", command=self.EDA, width=11, height=2)
        self.button3 = tk.Button(self.master, text="Car Racing", command=self.CarRacingBoy, width=11, height=2)
        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_application, width=11, height=2)

        # Đặt ba nút vào cuối cùng và căn đều theo chiều dài
        self.button1.place(x=350, y=420)
        self.button2.place(x=450, y=420)
        self.button3.place(x=550, y=420)
        self.exit_button.place(x=850, y=420)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Background
        self.image = Image.open("img/1.png")
        tk_image = ImageTk.PhotoImage(self.image)

        canvas = Canvas(root, width=900, height=400)
        canvas.pack()

        canvas.create_image(0, 0, anchor="nw", image=tk_image)
        canvas.image = tk_image

    def FaceDetection(self):
        face_detector = CV.FaceDetector(self.master)
        face_detector.run_gui()

    def EDA(self):
        eda = EDA.DataPreprocessing(root)

    def CarRacingBoy(self):
        # Ẩn cửa sổ Tkinter
        self.master.withdraw()
        # Tạo một thể hiện của RacingGame
        CarRacing.GameOptionsForm(self.master)

    def exit_application(self):
        # Kết thúc ứng dụng khi nút Exit được nhấn
        self.master.destroy()


root = tk.Tk()
app = MyGUI(root)
root.mainloop()
