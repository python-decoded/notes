import turtle
import time


class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("cyan")
        self.penup()

        self.hp = 100
        self.move_speed = 4
        self.pressed_keys = {"w": False, "a": False, "s": False, "d": False}

    def key_press(self, k):
        self.pressed_keys[k] = True

    def key_release(self, k):
        self.pressed_keys[k] = False

    def update(self):
        if self.pressed_keys["w"]:
            self.sety(self.ycor() + self.move_speed)
        if self.pressed_keys["s"]:
            self.sety(self.ycor() - self.move_speed)
        if self.pressed_keys["a"]:
            self.setx(self.xcor() - self.move_speed)
        if self.pressed_keys["d"]:
            self.setx(self.xcor() + self.move_speed)


class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 600)
        self.screen.title("Top Down Shooter - Turtle")
        self.screen.bgcolor("black")
        self.screen.tracer(0)  # turtle animation off

        self.player = Player()

        self.screen.listen()
        self.screen.onkeypress(lambda: self.player.key_press("w"), "w")
        self.screen.onkeypress(lambda: self.player.key_press("a"), "a")
        self.screen.onkeypress(lambda: self.player.key_press("s"), "s")
        self.screen.onkeypress(lambda: self.player.key_press("d"), "d")
        self.screen.onkeyrelease(lambda: self.player.key_release("w"), "w")
        self.screen.onkeyrelease(lambda: self.player.key_release("a"), "a")
        self.screen.onkeyrelease(lambda: self.player.key_release("s"), "s")
        self.screen.onkeyrelease(lambda: self.player.key_release("d"), "d")

    def update(self):
        if self.player.hp > 0:
            self.player.update()

        self.screen.update()

    def run(self):
        while True:
            time.sleep(0.02)  # 20 FPS
            self.update()


game = Game()
game.run()
turtle.done()
