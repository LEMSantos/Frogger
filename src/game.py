import sys

import pygame

from settings import GAME_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.sprites.player import Player


class Game:
    def __init__(self):
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.__display_surface = pygame.display.get_surface()
        self.__clock = pygame.time.Clock()

        self.__groups = self.__init_groups()
        self.__sprites = self.__init_sprites()

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __init_groups(self) -> dict[str, pygame.sprite.Group]:
        return {
            "all_sprites": pygame.sprite.Group(),
        }

    def __init_sprites(self) -> dict[str, pygame.sprite.Sprite]:
        return {
            "player": Player((600, 400), self.__groups["all_sprites"]),
        }

    def __update_groups(self, dt) -> None:
        for group in self.__groups.values():
            group.update(dt=dt)

    def __draw_groups(self, surface: pygame.Surface) -> None:
        for group in self.__groups.values():
            group.draw(surface)

    def run(self) -> None:
        while True:
            self.__handle_events()

            dt = self.__clock.tick() / 1000

            self.__display_surface.fill("black")

            self.__update_groups(dt)
            self.__draw_groups(self.__display_surface)

            pygame.display.update()
