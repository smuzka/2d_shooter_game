import pygame
from enemies.enemy import EnemyInterface

class Zombie(EnemyInterface):
    def __init__(self, screen_width, screen_height, speed=2, health=100, damage=10, scale_factor=1):
        self.original_image = pygame.image.load('images/zombie.png').convert_alpha()
        self.image = self.original_image

        super().__init__(screen_width, screen_height, 100)

        self.health = health
        self.max_health = health
        self.speed = speed
        self.damage = damage
        self.scale_factor = scale_factor
        new_size = (int(self.original_image.get_width() * self.scale_factor),
                    int(self.original_image.get_height() * self.scale_factor))
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, player_rect, other_enemies):
        super().update(player_rect, other_enemies)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)
