from pygame.sprite import Sprite
from pygame.surface import Surface


class SimpleObject(Sprite):
    def __init__(
        self, surface: Surface, position: tuple[float, float], *groups
    ) -> None:
        super().__init__(*groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)


class LongObject(Sprite):
    def __init__(
        self, surface: Surface, position: tuple[float, float], *groups
    ) -> None:
        super().__init__(*groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)

        self.hitbox = self.rect.inflate(-self.rect.width * 0.8, -self.rect.height / 2)
        self.hitbox.bottom = self.rect.bottom - 10
