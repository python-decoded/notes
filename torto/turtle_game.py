import turtle
import time


class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 600)
        self.screen.title("Top Down Shooter - Turtle")
        self.screen.bgcolor("black")
        self.screen.tracer(0)  # turtle animation off

    def update(self):

        self.screen.update()

    def run(self):
        while True:
            time.sleep(0.02)  # 20 FPS
            self.update()


game = Game()
game.run()
turtle.done()
