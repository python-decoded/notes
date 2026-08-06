import time
import curses
from copy import deepcopy

LEVELS = [
    {
        "width": 6, "height": 6, "player": (1, 1),
        "walls": [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
            (0, 1), (5, 1), (0, 2), (3, 2), (5, 2),
            (0, 3), (5, 3), (0, 4), (5, 4),
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)
        ],
        "boxes": [(2, 2)],
        "buttons": [(4, 3)]
    },
    {
        "width": 7, "height": 7,  "player": (3, 2),
        "walls": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (4, 1),
                  (0, 2), (4, 2), (5, 2), (6, 2), (0, 3), (6, 3),
                  (0, 4), (6, 4), (0, 5), (4, 5), (5, 5), (6, 5),
                  (0, 6), (1, 6), (2, 6), (3, 6)],
        "boxes": [(3, 3), (4, 3)],
        "buttons": [(2, 4), (3, 1)]
    },
    {
        "width": 13, "height": 9, "player": (7, 5),
        "walls": [(1, 0), (2, 0), (3, 0), (6, 0), (7, 0), (8, 0), (9, 0),
                  (1, 1), (3, 1), (4, 1), (5, 1), (6, 1), (9, 1), (10, 1),
                  (1, 2), (9, 2), (1, 3), (3, 3), (4, 3), (5, 3), (9, 3), (12, 4),
                  (0, 4), (1, 4), (5, 4), (6, 4), (7, 4), (9, 4), (10, 4), (11, 4),
                  (0, 5), (12, 5), (0, 6), (4, 6), (5, 6), (7, 6), (9, 6), (10, 6), (12, 6),
                  (0, 7), (2, 7), (3, 7), (4, 7), (5, 7), (12, 7), (0, 8), (1, 8), (2, 8),
                  (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8)],
        "boxes": [(3, 2)],
        "buttons": [(1, 7)]
    }
]


class Level:
    def __init__(self, stdscr: curses.window, width, height, player, walls, boxes, buttons,
                 start_level_func: callable, level_num: int):

        self.stdscr = stdscr
        self.start_level_func = start_level_func
        self.level_num = level_num

        self.field_width = width
        self.field_height = height

        self.player_pos = player
        self.walls = walls
        self.boxes = boxes
        self.buttons = buttons

    def get_new_dir(self) -> tuple[int, int] | None:

        key = self.stdscr.getch()  # отримати натиснуту клавішу
        directions = {
            curses.KEY_LEFT: (-1, 0),
            curses.KEY_RIGHT: (1, 0),
            curses.KEY_UP: (0, -1),
            curses.KEY_DOWN: (0, 1)
        }
        if key == ord("r"):
            self.start_level_func(self.level_num)
            return

        return directions.get(key)

    def act(self, dt):

        # якщо кнопки співпадають з ящиками - виграв
        if set(self.buttons) <= set(self.boxes):
            self.start_level_func(self.level_num + 1)
            return

        # якщо натиснута клавіша клавіатури
        shift = self.get_new_dir()
        if shift is None:
            return

        # вирахувати на яку клітину переміститься гравець
        dx, dy = shift
        player_new_position = self.player_pos[0] + dx, self.player_pos[1] + dy

        #     це в межах поля ?
        if player_new_position[0] not in range(self.field_width):
            return
        if player_new_position[1] not in range(self.field_height):
            return
        if player_new_position in self.walls:
            return

        if player_new_position in self.boxes:
            box_new_position = player_new_position[0] + dx, player_new_position[1] + dy
            if box_new_position[0] not in range(self.field_width):
                return
            if box_new_position[1] not in range(self.field_height):
                return
            if box_new_position in self.walls:
                return
            if box_new_position in self.boxes:
                return

            # рухаємо ящик - якщо треба
            self.boxes.remove(player_new_position)
            self.boxes.append(box_new_position)

        # рухаємо гравця
        self.player_pos = player_new_position

    def draw(self):

        field = [[" . "] * self.field_width
                 for _ in range(self.field_height)]
        for wall in self.walls:
            field[wall[1]][wall[0]] = "###"
        for button in self.buttons:
            field[button[1]][button[0]] = " o "
        for box in self.boxes:
            field[box[1]][box[0]] = "|X|"

        field[self.player_pos[1]][self.player_pos[0]] = "^_^"

        for y, row in enumerate(field, start=5):
            for x, ch in enumerate("".join(row), start=5):
                # if ch in "xo*":
                #     self.stdscr.addstr(y, x, ch, curses.color_pair(1))
                # elif ch in "@":
                #     self.stdscr.addstr(y, x, ch, curses.color_pair(2))
                # else:
                self.stdscr.addstr(y, x, ch)


class Game:

    level: Level

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.start_level(0)

    def start_level(self, idx):
        if idx >= len(LEVELS):
            print("Ви пройшли усі рівні, вітаю!!!")
            exit()

        level_data = deepcopy(LEVELS[idx])
        self.level = Level(self.stdscr, **level_data, start_level_func=self.start_level, level_num=idx)

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
            self.level.act(dt)
            self.level.draw()
            self.stdscr.refresh()
            prev_time = new_time
            time.sleep(0.05)  # FPS ~20


if __name__ == "__main__":
    runner = lambda stdscr: Game(stdscr).run()
    curses.wrapper(runner)
