import pygame
from powerUps.powerUpsGlobal import available_power_ups_names

class MultiShotPowerUp:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/multi_shot_up.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.type = available_power_ups_names['multi_shot']

    def draw(self, screen):
        screen.blit(self.image, self.rect)
