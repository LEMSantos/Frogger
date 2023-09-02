import sys
import random

import pygame

from src.sprites.car import Car
from src.core.camera import Camera
from src.sprites.player import Player
from settings import (
    GAME_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CAR_START_POSITIONS,
)


class Game:
    def __init__(self):
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.__display_surface = pygame.display.get_surface()
        self.__clock = pygame.time.Clock()

        self.__groups = self.__init_groups()
        self.__sprites = self.__init_sprites()
        self.__events = self.__init_events()

        self.__car_pos_list = []

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.__events["car_respawn"]:
                self.__spawn_car()

    def __init_groups(self) -> dict[str, pygame.sprite.Group]:
        return {
            "all_sprites": Camera(),
            "player": pygame.sprite.GroupSingle(),
            "cars": pygame.sprite.Group(),
        }

    def __init_events(self) -> dict[str, int]:
        car_respawn = pygame.event.custom_type()

        pygame.time.set_timer(car_respawn, 50)

        return {
            "car_respawn": car_respawn,
        }

    def __init_sprites(self) -> dict[str, pygame.sprite.Sprite]:
        return {
            "player": Player(
                (600, 400),
                self.__groups["all_sprites"],
                self.__groups["player"],
            ),
        }

    def __spawn_car(self) -> None:
        random_pos = random.choice(CAR_START_POSITIONS)

        if random_pos not in self.__car_pos_list:
            self.__car_pos_list.append(random_pos)
            Car(
                (random_pos[0], random_pos[1] + random.randint(-8, 8)),
                [self.__groups["cars"], self.__groups["all_sprites"]],
            )

        if len(self.__car_pos_list) > 5:
            del self.__car_pos_list[0]

    def run(self) -> None:
        while True:
            self.__handle_events()

            dt = self.__clock.tick() / 1000

            self.__display_surface.fill("black")

            self.__groups["all_sprites"].update(dt=dt)
            self.__groups["all_sprites"].customize_draw(
                surface=self.__display_surface,
                player=self.__sprites["player"],
            )

            pygame.display.update()
