import string
import pygame
import sys
import random

from pygame._sdl2 import controller

KEYS_LAYOUT = {
    'a': 'ф', 'b': 'и', 'c': 'с', 'd': 'в', 'e': 'у', 'f': 'а', 'g': 'п', 'h': 'р',
    'i': 'ш', 'j': 'о', 'k': 'л', 'l': 'д', 'm': 'ь', 'n': 'т', 'o': 'щ', 'p': 'з',
    'q': 'й', 'r': 'к', 's': 'і', 't': 'е', 'u': 'г', 'v': 'м', 'w': 'ц', 'x': 'ч',
    'y': 'н', 'z': 'я', '[': 'х', ']': 'ї', ';': 'ж', "'": 'є', ',': 'б', '.': 'ю'
}
LETTERS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя".upper()   # sorry ґ

# quick swich to english
# KEYS_LAYOUT = {}
# LETTERS = string.ascii_uppercase


# Initialize pygame
pygame.init()


class SurfaceContainer(pygame.sprite.Group):
    def __init__(self, x, y, width, height, bg = (0, 0, 0)):
        super().__init__()
        # Позиція контейнера на головному екрані
        self.x = x
        self.y = y
        self.bg = bg

        # Створюємо окрему поверхню (холст) для цього контейнера
        self.surface = pygame.Surface((width, height))

        # Додатково: дозволяємо прозорість для нашого холста
        self.surface.set_colorkey((0, 0, 0))  # Чорний колір стане прозорим

    def draw_to_screen(self, screen):
        """Малює спрайти всередині контейнера, а потім сам контейнер — на екран."""
        # 1. Очищаємо внутрішню поверхню перед кожним кадром
        self.surface.fill(self.bg)

        # Можна намалювати фон для самого контейнера (наприклад, сіра панель)
        # self.surface.fill((50, 50, 50))

        # 2. Малюємо всі спрайти групи НА ПОВЕРХНЮ КОНТЕЙНЕРА
        # Оскільки ми передаємо self.surface, координати rect кожного спрайта
        # рахуються відносно цього холста!
        super().draw(self.surface)

        # 3. Малюємо саму поверхню контейнера на ГОЛОВНИЙ ЕКРАН
        screen.blit(self.surface, (self.x, self.y))

class SpellBook:
    def __init__(self):
        super().__init__()
        self.keys = dict.fromkeys(["n", "s", "e",  "w", "ne", "se", "nw", "sw"], "")
        self.activated = []

        cell_size = 50
        self.key_icons = {
            "n": SquareWithLetter(cell_size, 0, cell_size, "A"),
            "ne": SquareWithLetter(0, 0, cell_size, "A"),
            "nw": SquareWithLetter(cell_size * 2, 0, cell_size, "A"),
            "s": SquareWithLetter(cell_size, cell_size * 2, cell_size, "A"),
            "se": SquareWithLetter(0, cell_size * 2, cell_size, "A"),
            "sw": SquareWithLetter(cell_size * 2, cell_size * 2, cell_size, "A"),
            "e": SquareWithLetter(0, cell_size, cell_size, "A"),
            "w": SquareWithLetter(cell_size * 2, cell_size, cell_size, "A"),
        }
        self.group = SurfaceContainer(x=20, y=20, width=cell_size * 3, height=cell_size * 3, bg = (30, 135, 123))
        self.group.add(*self.key_icons.values())

        for k in self.keys:
            self.randomize_key(k)
        print("BOOK AFTER SETUP: ", self.keys)

    def randomize_key(self, key):
        self.keys[key] = random.choice(list(set(LETTERS) - set(self.keys.values())))
        self.key_icons[key].letter = self.keys[key]
        self.key_icons[key].redraw_sprite()

    def reset(self):
        """
        Randomize activated keys, and reset all activation
        """
        if not self.activated:
            return

        for d in self.activated:
            self.randomize_key(d)
        self.activated = []

        print("BOOK AFTER RESET: ", self.keys)

    def activate(self, letter):
        for k, v in self.keys.items():
            if v == letter.upper():
                self.activated.append(k)

    def get_activated(self):
        return [k for k, v in self.keys.items() if k in self.activated]

    def update(self):
        for d, i in self.key_icons.items():
            if d in self.activated:
                i.redraw_sprite((39, 30, 30))
            else:
                i.redraw_sprite()


class UI(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()
        self.surface = pygame.display.get_surface()

        # Виправлено: використовуємо get_width() та get_height()
        self.height = height
        self.width = self.surface.get_width()

        # Створюємо прозору поверхню для спрайту
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((56, 56, 65))
        self.rect = self.image.get_rect()


class Controller:

    def __init__(self):
        self.holding_keys = set()
        self.pressed_keys = set()
        self.released_keys = set()

    def get_keys(self):
        return {"pressed": self.pressed_keys,
                "holding": self.holding_keys,
                "released": self.released_keys}

    def update(self):
        current_pressed = set()

        # 1. ОБРОБКА ЗВИЧАЙНИХ КЛАВІШ
        keys = pygame.key.get_pressed()
        for key_code in range(len(keys)):
            if keys[key_code]:
                key_name = pygame.key.name(key_code)
                button = KEYS_LAYOUT.get(key_name, key_name)
                current_pressed.add(button)

        # 2. ОБРОБКА SHIFT, CTRL, ALT (через get_mods)
        mods = pygame.key.get_mods()

        if mods & pygame.KMOD_SHIFT:
            current_pressed.add("shift")
        if mods & pygame.KMOD_CTRL:
            current_pressed.add("ctrl")
        if mods & pygame.KMOD_ALT:
            current_pressed.add("alt")

        # 3. ПОШУК КЛАВІШ (Математика множин)
        # Нові: є зараз, але не було в минулому кадрі
        new_keys = current_pressed - self.holding_keys

        # Виправлено: Відпущені — це ті, що БУЛИ в минулому кадрі, але ЗНИКЛИ зараз
        released_keys = self.holding_keys - current_pressed

        # 4. ЗБЕРЕЖЕННЯ СТАНУ В ОБ'ЄКТ
        self.pressed_keys = new_keys
        self.released_keys = released_keys
        self.holding_keys = current_pressed  # Оновлюємо історію в самому кінці

        # Повертаємо всі три стани
        return self.pressed_keys, self.holding_keys, self.released_keys


class Player(pygame.sprite.Sprite):

    def __init__(self, game, position):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.color.Color("red"))

        self.picture = pygame.image.load("./src/player.png").convert_alpha()
        self.picture = pygame.transform.scale(self.picture, (100, 100))

        self.rect = self.image.get_rect()

        self.rect.center = position
        self.target = position
        self.speed = 1

        self.controller = Controller()

        self.letters_near = set()
        self.shifted_keys = []

        self.enter_spells = False
        self.enter_spell_keys = []

        self.spell_book = SpellBook()

    def move_to(self, rect, target, speed):
        """
        Рухає rect у напрямку target із заданою швидкістю.
        rect: pygame.Rect (об'єкт, який рухається)
        target: pygame.Rect або tuple/list (координати цілі, наприклад, [x, y])
        speed: int або float (швидкість руху)
        """
        # 1. Отримуємо точку, куди треба йти (працює і з Rect, і з кортежем типу (x, y))
        target_pos = pygame.math.Vector2(target.center if hasattr(target, 'center') else target)
        current_pos = pygame.math.Vector2(rect.center)

        # 2. Рахуємо вектор напрямку та відстань
        direction = target_pos - current_pos
        distance = direction.length()

        # 3. Рухаємося, якщо ми ще не в цілі
        if distance > 0:
            if distance <= speed:
                # Якщо ціль ближче, ніж наш крок, просто стаємо в центр цілі
                rect.center = (round(target_pos.x), round(target_pos.y))
            else:
                # Нормалізуємо напрямок (робимо довжину 1) і множимо на швидкість
                new_pos = current_pos + direction.normalize() * speed
                # Округляємо та записуємо нові координати в rect
                rect.center = (round(new_pos.x), round(new_pos.y))

    def _update(self, dt: float):
        """
        1. update controls
        2. update player behavior
        3. process - ENTER state
        4. process - shift state
        5. process simple actions - and move to ENTER or SHIFT states if needed
        """

        self.controller.update()

        if self.rect.center != self.target:
            self.move_to(self.rect, self.target, self.speed * dt)
            return


        #     self.rect.x = self.target[0]
        #     return

        # Player UI
        if self.enter_spells:
            self.image.fill(pygame.color.Color("green"))
        elif "shift" in self.controller.holding_keys:
            self.image.fill(pygame.color.Color("yellow"))
        else:
            self.image.fill(pygame.color.Color("red"))

        # Cells in radius
        cells = self.game.grid.get_cells_by_coord(*self.rect.center, distance=self.game.grid.cell_size * 1.1)
        for c in self.game.grid.squares_group:
            if c.rect.center == self.rect.center:
                c.always_visible = True
                c.alpha = int(min(255, c.alpha * 2 + 10))
                c.redraw_sprite((0, 0, 255, c.alpha))
            elif c in cells:
                c.always_visible = True
                c.alpha = int(min(255, c.alpha * 2 + 10))
                c.redraw_sprite((0, 0, 255, c.alpha))
            elif c.always_visible is False:
                c.alpha = int(max(0, c.alpha / 2 - 10))
                c.redraw_sprite((0, 0, 255, c.alpha))
            else:
                c.alpha = int(min(255, c.alpha * 2 + 10))
                c.redraw_sprite((100, 100, 100, c.alpha))

        # PROCESS SPELLS MODE
        if self.enter_spells:
            # go from ENTER MODE
            if "return" in self.controller.pressed_keys:
                self.enter_spells = False
                print("ENTERED MESSAGE: ", self.enter_spell_keys)
                return

            self.enter_spell_keys.extend(self.controller.pressed_keys)
            return   #  STILL IN ENTER SPELLS MODE

        # ======================================================
        # alL further logic is blocked by enter spell mode
        # it makes sense to introduce some strategy here.
        # ======================================================

        # ENTER SPELLS MODE
        if "return" in self.controller.pressed_keys:
            self.enter_spells = True
            self.enter_spell_keys = []
            self.shifted_keys = []  # ignore shifted keys input if in enter spell mode,
            return

        if "shift" in self.controller.pressed_keys:
            print("holding shift")
            self.shifted_keys = []
            self.spell_book.reset()
            return
        if "shift" in self.controller.holding_keys:
            self.shifted_keys.extend(self.controller.pressed_keys)

            for k in self.controller.pressed_keys:
                self.spell_book.activate(k)
            return

        if "shift" in self.controller.released_keys:
            print("released shift: ", self.shifted_keys)
            print("ACTIVATED: ", self.spell_book.get_activated())
            self.spell_book.reset()
            return

        # ======================================================
        # alL further logic is blocked by shifted key pressed spell mode
        # it makes sense to introduce some strategy here.
        # ======================================================

        # ENTER SPELLS MODE
        # ENTER SPELLS MODE - RESET ALL SHIFTED
        if "return" in self.controller.pressed_keys:
            self.enter_spells = True
            self.enter_spell_keys = []
            self.spell_book.reset()
            return

        # PROCESS common mode --------------------------------------------------------------------------
        cells = self.game.grid.get_cells_by_coord(*self.rect.center, distance=self.game.grid.cell_size * 1.1)   # 4 arrount

        # DEBUG
        letters_near = {c.letter for c in cells}
        if letters_near != self.letters_near:
            print(letters_near)
            self.letters_near = letters_near

        for c in cells:
            if c.rect.center == self.rect.center:
                continue

            # print(c.letter, self.controller.pressed_keys)
            if c.letter.lower() in self.controller.pressed_keys:
                self.target = c.rect.center


        #     cells = [c for c in self.game.grid.get_cells_by_coord(*self.rect.center, distance=100)
        #
        # print(sorted([c.letter for c in cells]))

        # self.get_colliding_sprites_with_distances(self.player, self.game)

        # PROCESS common mode ends here ---------------------------------------------------------------------

    def update(self, dt: float):

        self._update(dt)
        self.game.screen.blit(self.picture, (self.rect.x - 25, self.rect.y - 45))

        self.spell_book.update()
        self.spell_book.group.draw_to_screen(self.game.screen)


class SquareWithLetter(pygame.sprite.Sprite):

    letter_size = 0.5
    always_visible = False
    alpha = 255

    def __init__(self, x, y, square_size, letter=None):
        super().__init__()

        self.letter = letter or random.choice(LETTERS)
        self.square_size = square_size

        # 1. Створюємо поверхню (полотно) для нашого спрайту
        self.image = pygame.Surface((square_size, square_size), pygame.SRCALPHA)

        # 2. Створюємо rect для керування позицією квадрата
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Малюємо квадрат і літеру ОДИН раз при створенні на self.image
        self.redraw_sprite()

    def redraw_sprite(self, color=(0, 0, 255)):
        """Малює квадрат та літеру на власній поверхні спрайту"""

        # Очищаємо поверхню (робимо її прозорою перед малюванням)
        self.image.fill((0, 0, 0, 0))

        # Малюємо квадрат (координати 0, 0, бо малюємо всередині самого спрайту)
        pygame.draw.rect(self.image, color, (0, 0, self.square_size, self.square_size))

        # Малюємо літеру по центру спрайту
        font = pygame.font.Font(None, int(self.square_size * self.letter_size))
        text_surface = font.render(self.letter, True, (255, 255, 255))  # Білий текст
        text_rect = text_surface.get_rect(center=(self.square_size // 2, self.square_size // 2))

        # оновлюємо лише цей шматок екрану.
        self.image.blit(text_surface, text_rect)

    def update(self, *args, **kwargs):
        ...


class Grid:

    def __init__(self, cell_size=60, padding = (0, 0),
                 rows = 9, cols = 12, spacing = (0, 0),
                 h_align="left", v_align="top",
                 surface: pygame.surface.Surface | None = None):

        self.surface = surface or pygame.display.get_surface()

        self.offset = padding  # external border of grid
        self.cell_size = cell_size
        self.spacing = spacing
        self.rows = rows
        self.cols = cols

        self.v_align = v_align  # center, top, bottom
        self.h_align = h_align  # left, center, right

        self.squares_group = self.prepare_squares()
        for s in self.squares_group:
            self.randomize_letter(s)

    @property
    def height(self):
        return self.offset[1] * 2 + (self.spacing[1] + self.cell_size) * self.rows - self.spacing[1]

    @property
    def width(self):
        return self.offset[0] * 2 + (self.spacing[0] + self.cell_size) * self.cols - self.spacing[0]

    def get_cells_by_coord(self, x, y, distance=None) -> list[SquareWithLetter]:
        # РЕЖИМ 1: Якщо відстань НЕ вказана, шукаємо одну клітинку під точкою

        if distance is None:
            for sprite in self.squares_group:
                if sprite.rect.collidepoint(x, y):
                    return sprite
            return None

        # РЕЖИМ 2: Якщо відстань вказана, шукаємо ВСІ клітинки в радіусі
        cells_in_radius = []
        target_vector = pygame.math.Vector2(x, y)

        for sprite in self.squares_group:
            sprite_vector = pygame.math.Vector2(sprite.rect.center)

            # Рахуємо відстань від точки (x, y) до центру клітинки
            if target_vector.distance_to(sprite_vector) <= distance:
                cells_in_radius.append(sprite)

        return cells_in_radius

    def randomize_letter(self, s):

        detection_zone = s.rect.inflate(200, 200)

        neighbor_letters = {sprite.letter for sprite in self.squares_group
                            if detection_zone.colliderect(sprite.rect) and s is not sprite}

        if s.letter in neighbor_letters:
            s.letter = random.choice(list(set(LETTERS) - neighbor_letters))
            # s.redraw_sprite((123, 123, 123))

    def prepare_squares(self):

        _x_offset, _y_offset, screen_width, screen_height, = self.surface.get_rect()

        if self.h_align == "center":
            _x_offset += -self.width // 2 + screen_width // 2
        elif self.h_align == "right":
            _x_offset +=  screen_width - self.width

        if self.v_align == "center":
            _y_offset += -self.height // 2 + screen_height // 2
        elif self.v_align == "bottom":
            _y_offset +=  screen_height - self.height

        squares = []
        for row in range(self.rows):
            for col in range(self.cols):
                x = _x_offset + self.offset[0] + col * self.spacing[0] + col * self.cell_size
                y = _y_offset + self.offset[1] + row * self.spacing[1] + row * self.cell_size
                squares.append(SquareWithLetter(x, y, self.cell_size))

        return pygame.sprite.Group(squares)

    def update(self):

        # for s in self.squares_group:
        #     if s.rect.collidepoint(*pygame.mouse.get_pos()):
        #
        #         detection_zone = s.rect.inflate(200, 200)
        #         neighbors = [sprite for sprite in self.squares_group
        #                      if detection_zone.colliderect(sprite.rect)]
        #         for n in neighbors:
        #             n.redraw_sprite((55, 55, 55))
        #
        #         s.redraw_sprite((123, 123, 123))

        self.squares_group.update()
        self.squares_group.draw(self.surface)

    # @classmethod
    # def get_square_size(cls, cell_size=60, offset = (40, 40), rows = 9, cols = 12,  spacing = 40):
    #     # you have window width, cols count, spacing,
    #
    #     # evaluate
    #     ...

    def get_neighbors(self):
        ...


class Game:

    def __init__(self):
        width, height = 1180, 720

        # self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)
        self.screen = pygame.display.set_mode((width, height))


        pygame.display.set_caption("Pygame-CE Template")
        self.grid = Grid(cell_size=80, cols=12, rows=6,
                         spacing=(5, 5), padding=(10, 20),
                         h_align="center", v_align="bottom")

    def main(self):
        clock = pygame.time.Clock()
        running = True

        ui = UI(self.screen.height - self.grid.height)
        ui_group = pygame.sprite.Group(ui)
        player = Player(self, random.choice(self.grid.squares_group.sprites()).rect.center)
        dt = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False


                # # спрацьовує лише для івента, івентів не так зазвичай і багато.
                # elif event.type == pygame.KEYDOWN:
                #     key_name = pygame.key.name(event.key).upper()
                #
                #     if len(key_name) == 1 and key_name in string.ascii_uppercase:
                #         ...
                #         # valid_targets = pygame.sprite.spritecollide(
                #         #     player, enemies_group, False,
                #         #     collided=pygame.sprite.collide_circle_ratio(MAX_DISTANCE / (player.size / 2))
                #         # )
                #         #
                #         # matching_targets = [e for e in valid_targets if e.letter == key_name]
                #         #
                #         # if matching_targets:
                #         #     # Тепер тут завжди буде максимум 1 об'єкт завдяки генерації, але сортування про всяк випадок залишаємо
                #         #     matching_targets.sort(key=get_distance)
                #         #     player.teleport_to(matching_targets[0])



            # Спрацьовує для кожного кадру - цикл з 27 літер,
            # може бути накладно кожен раз ітеруватись по усім літерам

            # Clear the screen
            self.screen.fill((255, 255, 255))
            ui_group.update()
            ui_group.draw(self.screen)

            self.grid.update()

            player.update(dt)

            # Update the display
            pygame.display.flip()
            dt = clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().main()
