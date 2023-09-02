import os
import sys

from pygame import quit as quit_game
from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.surface import Surface
from pygame.image import load as load_image
from pygame.key import get_pressed as get_pressed_key
from pygame.mask import from_surface as mask_from_surface

from src.sprites.car import Car


class Player(Sprite):
    def __init__(self, position: tuple[int, int], obstacles: Group, *groups):
        super().__init__(*groups)

        self.__obstacles = obstacles

        self.__animations = self.__import_assets()
        self.__animation_speed = 10
        self.__animation_index = 0
        self.__status = "down"

        self.image = self.__animations[self.__status][self.__animation_index]
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.mask = mask_from_surface(self.image)

        self.__direction = Vector2(0, 0)
        self.__pos = Vector2(self.rect.center)
        self.__speed = 200

    def __import_assets(self) -> dict[str, list[Surface]]:
        _path = "graphics/player"
        _animations = {}

        for root, dirs, files in os.walk(_path):
            if not dirs:
                _animations[root.split("/")[-1]] = [
                    load_image(f"{root}/{file}").convert_alpha()
                    for file in sorted(files)
                ]

        return _animations

    def __keyboard_input(self) -> None:
        keys_map = {
            (K_UP, "up"): Vector2(0, -1),
            (K_DOWN, "down"): Vector2(0, 1),
            (K_LEFT, "left"): Vector2(-1, 0),
            (K_RIGHT, "right"): Vector2(1, 0),
        }

        pressed_keys = get_pressed_key()

        self.__direction = Vector2(0, 0)

        for key, status in keys_map.keys():
            if pressed_keys[key]:
                self.__direction += keys_map[(key, status)]
                self.__status = status

    def __move(self, dt: int) -> None:
        if self.__direction.magnitude() > 0:
            self.__direction = self.__direction.normalize()

        self.__pos.x += self.__direction.x * self.__speed * dt
        self.rect.centerx = round(self.__pos.x)
        self.hitbox.centerx = self.rect.centerx
        self.__handle_collision("horizontal")

        self.__pos.y += self.__direction.y * self.__speed * dt
        self.rect.centery = round(self.__pos.y)
        self.hitbox.centery = self.rect.centery
        self.__handle_collision("vertical")

        self.mask = mask_from_surface(self.image)

    def __animate(self, dt: int) -> None:
        _animations = self.__animations[self.__status]

        self.__animation_index += self.__animation_speed * dt

        if self.__direction.magnitude() == 0:
            self.__animation_index = 0

        self.image = _animations[int(self.__animation_index % len(_animations))]
        self.mask = mask_from_surface(self.image)

    def __handle_collision(self, direction: str) -> None:
        for sprite in self.__obstacles.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if isinstance(sprite, Car):
                    quit_game()
                    sys.exit()

                if direction == "horizontal":
                    if self.__direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    else:
                        self.hitbox.left = sprite.hitbox.right
                else:
                    if self.__direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    else:
                        self.hitbox.bottom = sprite.hitbox.top

                self.__pos = Vector2(self.hitbox.center)
                self.rect.center = self.hitbox.center

    def __restrict_movement(self) -> None:
        if self.rect.left < 640:
            self.__pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640

        if self.rect.right > 2560:
            self.__pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560

        if self.rect.bottom > 3500:
            self.__pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

    def update(self, dt: int) -> None:
        self.__keyboard_input()
        self.__move(dt)
        self.__animate(dt)
        self.__restrict_movement()
