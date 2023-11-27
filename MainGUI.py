import tkinter as tk
from threading import Thread
import CarRacing

class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter Example")
        master.geometry("1000x500")

        # Tạo ba nút
        self.button1 = tk.Button(master, text="Button 1", command=self.button1_clicked, width=10)
        self.button2 = tk.Button(master, text="Button 2", command=self.button2_clicked, width=10)
        self.button3 = tk.Button(master, text="CarRacing", command=self.CarRacingBoy, width=10)

        # Đặt ba nút vào cuối cùng và căn đều theo chiều dài
        self.button1.place(x=450, y=400)
        self.button2.place(x=350, y=400)
        self.button3.place(x=550, y=400)

    def button1_clicked(self):
        print("Button 1 clicked")

    def button2_clicked(self):
        print("Button 2 clicked")

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


root = tk.Tk()
app = MyGUI(root)
root.mainloop()
