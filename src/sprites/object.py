from pygame.sprite import Sprite
from pygame.surface import Surface


class SimpleObject(Sprite):
    def __init__(
        self, surface: Surface, position: tuple[float, float], *groups
    ) -> None:
        super().__init__(*groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


class LongObject(Sprite):
    def __init__(
        self, surface: Surface, position: tuple[float, float], *groups
    ) -> None:
        super().__init__(*groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
