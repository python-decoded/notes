import turtle
import time
import random
from tkinter import Event


class Enemy(turtle.Turtle):
    def __init__(self, game: "Game"):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()

        self.game = game
        self.goto(random.randint(-self.screen.canvwidth, self.screen.canvwidth),
                  random.randint(-self.screen.canvheight, self.screen.canvheight))

    def update(self):
        self.setheading(self.towards(self.game.player))
        self.forward(1.4)
        if self.distance(self.game.player) <= 20:
            self.game.player.hp = max(0, self.game.player.hp - 1)


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
        self.enemies = [Enemy(self) for _ in range(5)]

        self.ui = turtle.Turtle()
        self.ui.goto(-350, 250)
        self.ui.color("white")
        self.ui.hideturtle()

        self.screen.listen()
        for i in "awsd":
            self.screen.getcanvas().bind(f"<KeyPress-{i}>", self.on_key_press)
            self.screen.getcanvas().bind(f"<KeyRelease-{i}>", self.on_key_release)

        self.mouse_left_hold = False
        self.screen.getcanvas().bind("<Button-1>", self.on_mouse_left_click)
        self.screen.getcanvas().bind("<ButtonRelease-1>", self.on_mouse_left_release)
        self.screen.getcanvas().bind("<Motion>", self.on_mouse_move)

    def on_mouse_move(self, event: Event):

        if self.player.hp > 0:
            x = event.x - self.screen.canvwidth
            y = self.screen.canvheight - event.y
            self.player.setheading(self.player.towards(x, y))

    def on_mouse_left_click(self, event: Event):
        self.mouse_left_hold = True

    def on_mouse_left_release(self, event: Event):
        self.mouse_left_hold = False

    def on_key_press(self, event: Event):
        self.player.key_press(event.keysym)

    def on_key_release(self, event: Event):
        self.player.key_release(event.keysym)

    def update(self):
        if self.player.hp > 0:
            self.player.update()
            for e in self.enemies:
                e.update()

        self.ui.clear()
        self.ui.write(f"HP: {self.player.hp}", font=("Arial", 16, "normal"))

        self.screen.update()

    def run(self):
        while True:
            time.sleep(0.02)  # 20 FPS
            self.update()


game = Game()
game.run()
turtle.done()
