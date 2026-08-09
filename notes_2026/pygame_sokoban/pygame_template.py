import sys
import pygame


CAPTION = "Назва вашої гри"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

    def update(self, dt):
        ...

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = clock.tick(60)  # 60 FPS
            self.update(dt)
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    Game().run()
