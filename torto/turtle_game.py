import turtle
import time


class Game:
    def __init__(self):
        self.screen = turtle.Screen()

    def update(self):
        ...

    def run(self):
        while True:
            time.sleep(0.02)  # 20 FPS
            self.update()


game = Game()
game.run()
turtle.done()
