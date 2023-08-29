from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.key import get_pressed as get_pressed_key
from pygame.mask import from_surface as mask_from_surface


class Player(Sprite):
    def __init__(self, position: tuple[int, int], *groups):
        super().__init__(*groups)

        self.image = Surface((50, 50))
        self.image.fill("red")

        self.rect = self.image.get_rect(center=position)
        self.mask = mask_from_surface(self.image)

        self.__direction = Vector2(0, 0)
        self.__pos = Vector2(self.rect.center)
        self.__speed = 400

    def __keyboard_input(self) -> None:
        keys_map = {
            K_UP: Vector2(0, -1),
            K_DOWN: Vector2(0, 1),
            K_LEFT: Vector2(-1, 0),
            K_RIGHT: Vector2(1, 0),
        }

        pressed_keys = get_pressed_key()

        self.__direction = Vector2(0, 0)

        for key in keys_map.keys():
            if pressed_keys[key]:
                self.__direction += keys_map[key]

    def __move(self, dt: int) -> None:
        direction = self.__direction

        if self.__direction.magnitude() > 0:
            direction = self.__direction.normalize()

        self.__pos += direction * self.__speed * dt

        self.rect.center = (round(self.__pos.x), round(self.__pos.y))
        self.mask = mask_from_surface(self.image)

    def update(self, dt: int) -> None:
        self.__keyboard_input()
        self.__move(dt)
