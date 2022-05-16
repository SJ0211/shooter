import pygame
import random

class Health(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("hp.png")
        self.rect = self.image.get_rect(x = x, y = y)
        self.radius = self.rect.width / 2
        self.x = x
        self.y = y



    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))

