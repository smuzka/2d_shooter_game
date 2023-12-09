import pygame
from enemies.enemy import EnemyInterface

class Zombie(EnemyInterface):
    def __init__(self, screen_width, screen_height):

        self.image = pygame.image.load('images/zombie.png').convert_alpha()

        super().__init__(screen_width, screen_height, 100)


        self.speed = 2  # Prędkość
        self.damage = 10  # Ilość zadawanych obrażeń

    def update(self, player_rect, other_enemies):
        super().update(player_rect, other_enemies)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)
