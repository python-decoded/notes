import time
import random
import curses


class Game:

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

        self.field_width = 10
        self.field_height = 6
        self.snake_len = 5
        self.snake_segments = [(0, 0)] * self.snake_len
        self.snake_dir = (1, 0)  # вправо
        self.snake_move_timeout = 1  # 1 крок на сек
        self.snake_sleep_time = 2  # сек.
        self.snake_alive = True
        self.apple = (3, 0)

    def get_apple_new_position(self):
        cells = {(x, y) for x in range(self.field_width)
                 for y in range(self.field_height)}
        cells -= set(self.snake_segments)
        return random.choice(list(cells))

    def get_snake_new_dir(self):

        key = self.stdscr.getch()  # отримати натиснуту клавішу
        directions = {
            curses.KEY_LEFT: (-1, 0),
            curses.KEY_RIGHT: (1, 0),
            curses.KEY_UP: (0, -1),
            curses.KEY_DOWN: (0, 1)
        }
        return directions.get(key, self.snake_dir)

    def act(self, dt):
        if not self.snake_alive:
            return

        self.snake_sleep_time -= dt
        if self.snake_sleep_time > 0:
            return

        self.snake_sleep_time += self.snake_move_timeout

        head, *body = self.snake_segments

        self.snake_dir = self.get_snake_new_dir()
        next_head = (head[0] + self.snake_dir[0],
                     head[1] + self.snake_dir[1])

        in_field = (next_head[0] in range(self.field_width)
                    and next_head[1] in range(self.field_height))
        if not in_field:
            self.snake_alive = False
            return

        self.snake_segments.insert(0, next_head)
        if next_head == self.apple:
            self.apple = self.get_apple_new_position()
            self.snake_len += 1
            self.snake_move_timeout *= 0.9

        self.snake_segments = self.snake_segments[:self.snake_len]
        if self.snake_segments[0] in self.snake_segments[1:]:
            self.snake_alive = False

    def draw(self):

        field = [[" . "] * self.field_width
                 for _ in range(self.field_height)]
        apple_x, apple_y = self.apple
        field[apple_y][apple_x] = " @ "

        snake_head, *snake_body = self.snake_segments
        for x, y in snake_body:
            field[y][x] = " o "

        field[snake_head[1]][snake_head[0]] = " * " if self.snake_alive else " x "

        for y, row in enumerate(field, start=5):
            for x, ch in enumerate("".join(row), start=5):
                if ch in "xo*":
                    self.stdscr.addstr(y, x, ch, curses.color_pair(1))
                elif ch in "@":
                    self.stdscr.addstr(y, x, ch, curses.color_pair(2))
                else:
                    self.stdscr.addstr(y, x, ch)

    def run(self):

        curses.curs_set(0)  # ховаємо курсор
        self.stdscr.nodelay(True)  # stdscr.getch() неблокуючий

        # кольори
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        prev_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - prev_time
            self.stdscr.clear()
            self.act(dt)
            self.draw()
            self.stdscr.refresh()
            prev_time = new_time
            time.sleep(0.05)  # FPS ~20


if __name__ == "__main__":
    runner = lambda stdscr: Game(stdscr).run()
    curses.wrapper(runner)
