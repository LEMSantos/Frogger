import os
import random

from pygame.math import Vector2
from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.image import load as load_image
from pygame.transform import flip as flip_surface
from pygame.mask import from_surface as mask_from_surface

from settings import WINDOW_WIDTH


class Car(Sprite):
    def __init__(self, position: tuple[int, int], *groups) -> None:
        super().__init__(*groups)

        self.__assets = self.__import_assets()

        self.image = random.choice(self.__assets)
        self.__direction = Vector2(1, 0)

        if Vector2(position).x > WINDOW_WIDTH:
            self.__direction = Vector2(-1, 0)
            self.image = flip_surface(self.image, True, False)

        self.rect = self.image.get_rect(center=position)
        self.mask = mask_from_surface(self.image)

        self.__pos = Vector2(self.rect.center)
        self.__speed = 300

    def __import_assets(self) -> list[Surface]:
        _path = "graphics/cars"

        return [
            load_image(f"{_path}/{image}").convert_alpha()
            for image in os.listdir(_path)
        ]

    def __move(self, dt: int) -> None:
        self.__pos += self.__direction * self.__speed * dt
        self.rect.center = (round(self.__pos.x), round(self.__pos.y))

    def update(self, dt: int) -> None:
        self.__move(dt)

        if not -200 < self.rect.x < 3400:
            self.kill()
