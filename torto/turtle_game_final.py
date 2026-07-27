import turtle
import random
from collections import defaultdict
from functools import partial
from tkinter import Event


FPS = 30
DT = 1 / FPS


class UI:

    font = ("Arial", 14, "bold")

    def __init__(self, game):
        self.game = game

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.color("white")

    def update(self):
        self.t.clear()
        self.t.goto(-380, 260)
        self.t.write(f"HP: {self.game.player.hp}        KILLED: {self.game.kills}", font=self.font)


class Controller:

    def __init__(self):
        self.pressed_keys = defaultdict(lambda: False)
        self.mouse_down = False

    def is_pressed(self, k) -> bool:
        return self.pressed_keys[k]

    def key_press(self, k):
        self.pressed_keys[k] = True

    def key_release(self, k):
        self.pressed_keys[k] = False

    def mouse_press(self, event: Event):
        self.mouse_down = True

    def mouse_release(self, event: Event):
        self.mouse_down = False


class Turtle(turtle.Turtle):

    def __init__(self, game, *args, **kwargs):
        self.game = game
        super().__init__(*args, **kwargs)

        self.penup()
        self.speed(0)

        self.setup()

    def setup(self):
        ...

    def update(self):
        ...

    def process_collision(self, other: "Turtle"):
        ...


class Player(Turtle):

    wait_fire_release = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape("triangle")
        self.color("cyan")

    def alive(self):
        return self.hp > 0

    def setup(self):
        self.hp = 100
        self.kills = 0
        self.move_speed = 80

        self.home()

    def rotate_towards_mouse_position(self, event: Event):
        if self.game.game_over:
            return

        x = event.x - self.game.screen.window_width() // 2
        y = self.game.screen.window_height() // 2 - event.y
        self.setheading(self.towards(x, y))

    def move(self):
        if self.game.controller.is_pressed("w"):
            self.sety(self.ycor() + self.move_speed * DT)
        if self.game.controller.is_pressed("s"):
            self.sety(self.ycor() - self.move_speed * DT)
        if self.game.controller.is_pressed("a"):
            self.setx(self.xcor() - self.move_speed * DT)
        if self.game.controller.is_pressed("d"):
            self.setx(self.xcor() + self.move_speed * DT)

    def fire_bullet(self):
        if self.wait_fire_release:
            if not self.game.controller.mouse_down:
                self.wait_fire_release = False
            return

        if not self.game.controller.mouse_down or self.game.game_over:
            return

        for b in self.game.bullets:
            if not b.isvisible():
                b.launch(self.position(), self.heading())
                break

        self.wait_fire_release = True

    def process_collision(self, other):

        if isinstance(other, Enemy):
            self.hp = max(0, self.hp - 1)
            if self.hp <= 0:
                self.game.game_over = True

        elif isinstance(other, SpeedPack):
            self.move_speed += 5
            other.spawn()
        elif isinstance(other, AmmoPack):
            self.game.bullets.append(Bullet(self.game))
            other.spawn()

    def update(self):
        self.move()
        self.fire_bullet()


class Enemy(Turtle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape("circle")
        self.color("red")
        self.spawn()

    def spawn(self):
        self.goto(random.randint(-380, 380), random.randint(-280, 280))

    def update(self):
        if self.game.game_over:
            return

        self.setheading(self.towards(self.game.player))
        self.forward(self.game.enemy_speed * DT)

    def process_collision(self, other: "Turtle"):
        if isinstance(other, Bullet):
            self.spawn()
            self.game.kills += 1


class SpeedPack(Turtle):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.shape("square")
        self.color("green")
        self.spawn()

    def spawn(self):
        self.goto(random.randint(-380, 380), random.randint(-280, 280))

    def update(self):
        self.left(4)


class AmmoPack(Turtle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shape("square")
        self.color("yellow")
        self.spawn()

    def spawn(self):
        self.goto(random.randint(-380, 380), random.randint(-280, 280))

    def update(self):
        self.left(4)


class Bullet(Turtle):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.shape("circle")
        self.color("yellow")
        self.shapesize(0.3)

        self.penup()
        self.hideturtle()

    def launch(self, position, angle):
        self.teleport(*position)
        self.setheading(angle)
        self.pendown()
        self.showturtle()

    def update(self):

        if not self.isvisible():
            return

        if self.game.game_over:
            return

        self.forward(240 * DT)

        if abs(self.xcor()) > 450 or abs(self.ycor()) > 350:
            self.hideturtle()
            self.penup()
            return

    def process_collision(self, other: "Turtle"):

        if not self.isvisible():
            return

        if isinstance(other, Enemy):
            self.hideturtle()
            self.penup()


class GameOverScreen(Turtle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color("white")
        self.hideturtle()

    def update(self):

        if not self.game.game_over:
            return

        self.clear()
        self.goto(0, 40)
        self.write("💀 GAME OVER 💀", align="center", font=("Arial", 34, "bold"))

        self.goto(0, -10)
        self.write(f"Вбито ворогів: {self.game.kills}", align="center", font=("Arial", 24, "normal"))

        self.goto(0, -60)
        self.write("Натисни R щоб перезапустити", align="center", font=("Arial", 18, "normal"))


class Game:

    kills: int
    enemy_speed: float
    game_over: bool

    def __init__(self):

        self.enemies = []
        self.bullets = [Bullet(self) for _ in range(6)]

        self.screen = self.setup_screen()

        self.hud = UI(self)
        self.game_over_screen = GameOverScreen(self)

        self.player = Player(self)
        self.controller = Controller()
        self.setup_listeners()

        self.speed_pack = SpeedPack(self)
        self.ammo_pack = AmmoPack(self)

        self.setup_game()

    def setup_screen(self):
        screen = turtle.Screen()

        screen.setup(800, 600)
        screen.title("Top-Down Shooter (Turtle)")
        screen.bgcolor("black")
        screen.tracer(0)  # turtle animation off
        return screen

    def setup_listeners(self):

        self.screen.listen()

        # KeyPress-a, KeyRelease-a - for keyboard events
        # ButtonPress-1, ButtonRelease-1, Motion, MouseWheel - for mouse events
        for k in "wasd":
            #  <KeyPress-%s> <KeyRelease-%s>
            self.screen.onkeypress(partial(self.controller.key_press, k), k)
            self.screen.onkeyrelease(partial(self.controller.key_release, k), k)

        self.screen.onkeypress(self.setup_game, "r")
        self.screen.getcanvas().bind("<Motion>", self.player.rotate_towards_mouse_position)
        self.screen.getcanvas().bind("<Button-1>", self.controller.mouse_press)
        self.screen.getcanvas().bind("<ButtonRelease-1>", self.controller.mouse_release)

    def setup_game(self):

        self.kills = 0
        self.enemy_speed = 38

        for b in self.bullets:
            b.hideturtle()
        for e in self.enemies:
            e.hideturtle()

        for b in self.bullets:
            b.clear()
        self.bullets = self.bullets[:6]

        self.enemies = [Enemy(self) for _ in range(5)]

        self.game_over = False
        self.game_over_screen.clear()
        self.hud.update()
        self.player.setup()

    def update(self):

        if not self.game_over:
            self.speed_pack.update()
            self.ammo_pack.update()
            self.player.update()

            for b in self.bullets[:]:
                b.update()

            for e in self.enemies[:]:
                e.update()

            self.enemy_speed += 2 * DT  # over time enemies speed raises
            self.precess_colision([self.player], [self.speed_pack, self.ammo_pack] + self.enemies)
            self.precess_colision(self.bullets, self.enemies)

        self.hud.update()
        self.game_over_screen.update()
        self.screen.update()

    def precess_colision(self, collection1: list[Turtle], collection2: list[Turtle]):
        for i in collection1[:]:
            for j in sorted(collection2[:], key=lambda i: i.distance(i.position())):
                if i.distance(*j.position()) < 20:
                    i.process_collision(j)
                    j.process_collision(i)

    def run(self):
        self.update()
        game.screen.ontimer(self.run, 1000 // FPS)


game = Game()
game.run()
turtle.done()
