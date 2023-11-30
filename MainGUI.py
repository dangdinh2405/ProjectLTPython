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
        master.title("Tkinter Example")
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
        face = CV.FaceDetector('1.mp4')
        face.detect_faces()

    def EDA(self):
        eda = EDA.DataPreprocessing(root)

    def CarRacingBoy(self):
        # Ẩn cửa sổ Tkinter
        self.master.withdraw()

        # Tạo một thể hiện của RacingGame
        car = CarRacing.RacingGame()

        # Chạy trò chơi trong một luồng riêng biệt
        game_thread = Thread(target=car.run_game)

        # Bắt đầu luồng trò chơi
        game_thread.start()

        # Đợi cho luồng trò chơi kết thúc và sau đó hiển thị lại cửa sổ Tkinter
        self.master.after(0, self.check_game_status, game_thread)

    def check_game_status(self, game_thread):
        # Kiểm tra trạng thái của luồng trò chơi
        if game_thread.is_alive():
            # Nếu trò chơi vẫn đang chạy, kiểm tra lại sau một khoảng thời gian nhất định
            self.master.after(100, self.check_game_status, game_thread)
        else:
            # Nếu trò chơi đã kết thúc, hiển thị lại cửa sổ Tkinter
            self.master.deiconify()

    def exit_application(self):
        # Kết thúc ứng dụng khi nút Exit được nhấn
        self.master.destroy()


root = tk.Tk()
app = MyGUI(root)
root.mainloop()
