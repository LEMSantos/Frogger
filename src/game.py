import sys

import pygame

from settings import GAME_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class Game:
    def __init__(self):
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.__display_surface = pygame.display.get_surface()
        self.__clock = pygame.time.Clock()

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self) -> None:
        while True:
            self.__handle_events()

            dt = self.__clock.tick() / 1000

            self.__display_surface.fill("black")

            pygame.display.update()
