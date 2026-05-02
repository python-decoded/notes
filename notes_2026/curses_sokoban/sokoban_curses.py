import time
import curses


class Level:
    def __init__(self, stdscr: curses.window, width, height, player, walls, boxes, buttons):
        self.stdscr = stdscr

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
        return directions.get(key)

    def act(self, dt):
        # якщо кнопки співпадають з ящиками - виграв
        if set(self.buttons) <= set(self.boxes):
            # todo запустити наступний рівень
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

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.level = Level(stdscr)

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
