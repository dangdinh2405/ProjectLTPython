from threading import Thread

import pygame
import sys
import random
from PIL import ImageTk, Image
from pygame.locals import *
import tkinter as tk

class RacingGame:
    def __init__(self, selected_fps, selected_bg, selected_car, selected_obstacles):
        pygame.init()
        self.WINDOWWIDTH = 400
        self.WINDOWHEIGHT = 600

        self.FPS = selected_fps.get()
        self.fpsClock = pygame.time.Clock()

        self.BGSPEED = 1.5
        self.BGIMG = pygame.image.load(selected_bg.get())

        self.CARIMG = pygame.image.load(selected_car.get())
        self.OBSTACLESIMG = pygame.image.load(selected_obstacles.get())

        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))


        pygame.display.set_caption('12 Dinh Dai Hai Dang Game ĐUA XE')

        self.show_settings_interface()
        self.bg = Background(self.BGSPEED, self.BGIMG, self.DISPLAYSURF)
        self.car = Car(self.WINDOWWIDTH, self.WINDOWHEIGHT, self.CARIMG, self.DISPLAYSURF)
        self.obstacles = Obstacles(self.WINDOWHEIGHT, self.OBSTACLESIMG,self.DISPLAYSURF)
        self.score = Score(self.DISPLAYSURF, self.WINDOWWIDTH, self.WINDOWHEIGHT, self.fpsClock, self.FPS, self.BGSPEED, self.BGIMG, self.CARIMG, self.OBSTACLESIMG)

    def show_settings_interface(self):
        # Hiển thị giao diện tùy chỉnh thông số
        # Các ô nhập liệu, nút và các phần tử giao diện người dùng khác có thể được thêm vào đây
        pass

    def run_game(self):
        self.score.game_start(self.bg)
        while True:
            self.score.game_play(self.bg, self.car, self.obstacles, self.score)
            self.score.game_over(self.bg, self.car, self.obstacles, self.score)


class Background:
    def __init__(self, BGSPEED, BGIMG, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.BGIMG = BGIMG
        self.BGSPEED = BGSPEED
        self.x = 0
        self.y = 0
        self.speed = self.BGSPEED
        self.img = self.BGIMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self):
        self.DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))
        self.DISPLAYSURF.blit(self.img, (int(self.x), int(self.y - self.height)))

    def update(self):
        self.y += self.speed

        if self.y > self.height:
            self.y -= self.height


class Car:
    def __init__(self, WINDOWWIDTH, WINDOWHEIGHT, CARIMG, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.CARIMG = CARIMG
        self.WINDOWHEIGHT = WINDOWHEIGHT
        self.WINDOWWIDTH = WINDOWWIDTH
        self.width = 40
        self.height = 60
        self.x = (self.WINDOWWIDTH - self.width) / 2
        self.y = (self.WINDOWHEIGHT - self.height) / 2
        self.speed = 3

    def draw(self):
        self.DISPLAYSURF.blit(self.CARIMG, (int(self.x), int(self.y)))

    def update(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft:
            self.x -= self.speed
        if moveRight:
            self.x += self.speed
        if moveUp:
            self.y -= self.speed
        if moveDown:
            self.y += self.speed
        if self.x < 80:
            self.x = 80
        if self.x + self.width > self.WINDOWWIDTH - 80:
            self.x = self.WINDOWWIDTH - 80 - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > self.WINDOWHEIGHT:
            self.y = self.WINDOWHEIGHT - self.height

class Obstacles:
    def __init__(self, WINDOWHEIGHT, OBSTACLESIMG, DISPLAYSURF):
        self.OBSTACLESIMG = OBSTACLESIMG
        self.DISPLAYSURF = DISPLAYSURF
        self.WINDOWHEIGHT = WINDOWHEIGHT
        self.width = 40
        self.height = 60
        self.distance = 200
        self.speed = 2
        self.changeSpeed = 0.001
        self.ls = []
        for i in range(5):
            y = -self.height - i * self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])

    def draw(self):
        for i in range(5):
            x = int(80 + self.ls[i][0] * 60 + (60 - self.width) / 2)
            y = int(self.ls[i][1])
            self.DISPLAYSURF.blit(self.OBSTACLESIMG, (x, y))

    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.changeSpeed
        if self.ls[0][1] > self.WINDOWHEIGHT:
            self.ls.pop(0)
            y = self.ls[3][1] - self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])

class Score:
    def __init__(self, DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT, fpsClock, FPS, BGSPEED, BGIMG, CARIMG, OBSTACLESIMG):
        self.OBSTACLESIMG = OBSTACLESIMG
        self.CARIMG = CARIMG
        self.WINDOWHEIGHT = WINDOWHEIGHT
        self.BGIMG = BGIMG
        self.BGSPEED = BGSPEED
        self.FPS = FPS
        self.fpsClock = fpsClock
        self.WINDOWWIDTH = WINDOWWIDTH
        self.DISPLAYSURF = DISPLAYSURF
        self.score = 0

    def draw(self):
        font = pygame.font.SysFont('consolas', 30)
        score_surface = font.render('Score: ' + str(int(self.score)), True, (0, 0, 0))
        self.DISPLAYSURF.blit(score_surface, (10, 10))

    def update(self):
        self.score += 0.02

    def rect_collision(self, rect1, rect2):
        if rect1[0] <= rect2[0] + rect2[2] and rect2[0] <= rect1[0] + rect1[2] and rect1[1] <= rect2[1] + rect2[3] and \
                rect2[1] <= rect1[1] + rect1[3]:
            return True
        return False

    def is_gameover(self, car, obstacles):
        car_rect = [car.x, car.y, car.width, car.height]
        for i in range(5):
            x = int(80 + obstacles.ls[i][0] * 60 + (60 - obstacles.width) / 2)
            y = int(obstacles.ls[i][1])
            obstacles_rect = [x, y, obstacles.width, obstacles.height]
            if self.rect_collision(car_rect, obstacles_rect):
                return True
        return False

    def game_over(self, bg, car, obstacles, score):
        font = pygame.font.SysFont('consolas', 60)
        heading_surface = font.render('GAMEOVER', True, (255, 0, 0))
        heading_size = heading_surface.get_size()
        font = pygame.font.SysFont('consolas', 20)
        comment_surface = font.render('Press "space" to replay', True, (0, 0, 0))
        comment_size = comment_surface.get_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == K_SPACE:
                        return
                    elif event.key == K_q:
                        pygame.quit()
                        quit()
            bg.draw()
            car.draw()
            obstacles.draw()
            score.draw()
            self.DISPLAYSURF.blit(heading_surface, (int((self.WINDOWWIDTH - heading_size[0]) / 2), 100))
            self.DISPLAYSURF.blit(comment_surface, (int((self.WINDOWWIDTH - comment_size[0]) / 2), 400))
            pygame.display.update()
            self.fpsClock.tick(self.FPS)

    def game_start(self, bg, ):
        bg.__init__(self.BGSPEED, self.BGIMG, self.DISPLAYSURF)
        font = pygame.font.SysFont('consolas', 60)
        heading_surface = font.render('RACING', True, (255, 0, 0))
        heading_size = heading_surface.get_size()
        font = pygame.font.SysFont('consolas', 20)
        comment_surface = font.render('Press "space" to play', True, (0, 0, 0))
        comment_size = comment_surface.get_size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == K_SPACE:
                        return
                    if event.key == K_q:
                        pygame.quit()
                        quit()
            bg.draw()
            self.DISPLAYSURF.blit(heading_surface, (int((self.WINDOWWIDTH - heading_size[0]) / 2), 100))
            self.DISPLAYSURF.blit(comment_surface, (int((self.WINDOWWIDTH - comment_size[0]) / 2), 400))
            pygame.display.update()
            self.fpsClock.tick(self.FPS)

    def game_play(self, bg, car, obstacles, score):
        car.__init__(self.WINDOWWIDTH, self.WINDOWHEIGHT, self.CARIMG, self.DISPLAYSURF)
        obstacles.__init__(self.WINDOWHEIGHT, self.OBSTACLESIMG, self.DISPLAYSURF)
        bg.__init__(self.BGSPEED, self.BGIMG, self.DISPLAYSURF)
        score.__init__(self.DISPLAYSURF, self.WINDOWWIDTH, self.WINDOWHEIGHT, self.fpsClock, self.FPS, self.BGSPEED, self.BGIMG, self.CARIMG, self.OBSTACLESIMG)
        move_left = False
        move_right = False
        move_up = False
        move_down = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        move_left = True
                    if event.key == K_RIGHT:
                        move_right = True
                    if event.key == K_UP:
                        move_up = True
                    if event.key == K_DOWN:
                        move_down = True
                    if event.key == K_q:
                        pygame.quit()
                        quit()
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        move_left = False
                    if event.key == K_RIGHT:
                        move_right = False
                    if event.key == K_UP:
                        move_up = False
                    if event.key == K_DOWN:
                        move_down = False
            if self.is_gameover(car, obstacles):
                return
            bg.draw()
            bg.update()
            car.draw()
            car.update(move_left, move_right, move_up, move_down)
            obstacles.draw()
            obstacles.update()
            self.draw()
            self.update()
            pygame.display.update()
            self.fpsClock.tick(self.FPS)


class GameOptionsForm:
    def __init__(self, root):
        self.root = root
        self.master = tk.Toplevel(self.root)
        self.master.title("Game Options")
        self.master.geometry("400x600")
        self.selected_fps = tk.IntVar(value=60)

        # Tạo các Radiobutton với giá trị tương ứng là số là xe
        tk.Radiobutton(self.master, text="60 fps", variable=self.selected_fps, value=60).grid(row=1, column=1)
        tk.Radiobutton(self.master, text="120 fps", variable=self.selected_fps, value=120).grid(row=1, column=2)

        self.fps_label = tk.Label(self.master, text="Frames per second:")
        self.fps_label.grid(row=1, column=0, padx=10, pady=5)

        self.selected_bg = tk.StringVar(value='img/background.png')

        # Tạo các Radiobutton với giá trị tương ứng là số làn xe
        tk.Radiobutton(self.master, text="background 1", variable=self.selected_bg, value='img/background.png').place(x=100,y=50)
        tk.Radiobutton(self.master, text="background 2", variable=self.selected_bg, value='img/background1.png').place(x=210,y=50)

        self.background_image_label = tk.Label(self.master, text="Background")
        self.background_image_label.place(x=20,y=50)

        self.selected_car = tk.StringVar(value='img/car.png')

        tk.Radiobutton(self.master, text="car", variable=self.selected_car, value='img/car.png').place(x=100,y=190)
        tk.Radiobutton(self.master, text="car1", variable=self.selected_car, value='img/car1.png').place(x=200,y=190)
        tk.Radiobutton(self.master, text="car2", variable=self.selected_car, value='img/car2.png').place(x=300, y=190)

        self.car_type_label = tk.Label(self.master, text="Car:")
        self.car_type_label.place(x=20,y=190)

        self.selected_obstacles= tk.StringVar(value='img/obstacles.png')

        tk.Radiobutton(self.master, text="obstacles", variable=self.selected_obstacles, value='img/obstacles.png').place(x=100, y=310)
        tk.Radiobutton(self.master, text="obstacles1", variable=self.selected_obstacles, value='img/obstacles1.png').place(x=200, y=310)
        tk.Radiobutton(self.master, text="obstacles2", variable=self.selected_obstacles, value='img/obstacles2.png').place(x=300, y=310)

        self.car_type_label = tk.Label(self.master, text="Obstacles:")
        self.car_type_label.place(x=20, y=310)

        self.ok_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.ok_button.place(x=100, y=500)
        self.cancel_button = tk.Button(self.master, text="Cancel", command=self.cancel_button_handler)
        self.cancel_button.place(x=250, y=500)

        img = Image.open('img/background.png')
        img = img.resize((100, 100), resample=Image.LANCZOS)

        self.image = ImageTk.PhotoImage(img)

        # Hiển thị hình ảnh trên form
        self.label = tk.Label(self.master, image=self.image)
        self.label.place(x=100,y=70)

        img2 = Image.open('img/background1.png')
        img2 = img2.resize((100, 100), Image.LANCZOS)

        # Chuyển ảnh sang định dạng PhotoImage
        self.image2 = ImageTk.PhotoImage(img2)

        # Hiển thị hình ảnh trên form
        self.label2 = tk.Label(self.master, image=self.image2)
        self.label2.place(x=210,y=70)

        img_car = Image.open('img/car.png')

        self.image_car = ImageTk.PhotoImage(img_car)

        self.lb1 = tk.Label(self.master, image=self.image_car)
        self.lb1.place(x=100, y=220)

        img_car2 = Image.open('img/car1.png')

        self.image_car2 = ImageTk.PhotoImage(img_car2)

        self.lb2 = tk.Label(self.master, image=self.image_car2)
        self.lb2.place(x=200, y=220)

        img_car3 = Image.open('img/car2.png')

        self.image_car3 = ImageTk.PhotoImage(img_car3)

        self.lb3 = tk.Label(self.master, image=self.image_car3)
        self.lb3.place(x=300, y=220)

        img_obstacles = Image.open('img/obstacles.png')

        self.image_obstacles = ImageTk.PhotoImage(img_obstacles)

        self.lbo1 = tk.Label(self.master, image=self.image_obstacles)
        self.lbo1.place(x=120, y=350)

        img_obstacles1 = Image.open('img/obstacles1.png')

        self.image_obstacles1 = ImageTk.PhotoImage(img_obstacles1)

        self.lbo2 = tk.Label(self.master, image=self.image_obstacles1)
        self.lbo2.place(x=220, y=350)

        img_obstacles2 = Image.open('img/obstacles2.png')

        self.image_obstacles2 = ImageTk.PhotoImage(img_obstacles2)

        self.lbo3 = tk.Label(self.master, image=self.image_obstacles2)
        self.lbo3.place(x=320, y=350)

    def cancel_button_handler(self):
        self.master.destroy()
        self.root.deiconify()

    def start_game(self):
        self.master.destroy()
        fps = self.selected_fps
        background_image = self.selected_bg
        car_type = self.selected_car
        obstacles_type = self.selected_obstacles

        run_game = RacingGame(fps, background_image, car_type,  obstacles_type)

        game_thread = Thread(target=run_game.run_game)
        game_thread.start()

        self.master.after(0, self.check_game_status, game_thread)

    def check_game_status(self, game_thread):
        if game_thread.is_alive():
            # Nếu luồng trò chơi vẫn đang chạy, đợi thêm và kiểm tra lại
            self.master.after(100, self.check_game_status, game_thread)
        else:
            # Nếu luồng trò chơi đã kết thúc, hiển thị lại cửa sổ Tkinter
            self.root.deiconify()


if __name__ == '__main__':
    root = tk.Tk()
    game = GameOptionsForm(root)
    root.mainloop()

