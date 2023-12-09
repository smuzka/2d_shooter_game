import pygame
from enemies.enemy import EnemyInterface
from enemies.bullet import Bullet

class Ranger(EnemyInterface):
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load('images/ranger.png').convert_alpha()
        super().__init__(screen_width, screen_height, 50)

        self.speed = 1
        self.damage = 10
        # Time in milliseconds between shots
        self.shoot_cooldown = 1000
        self.last_shot_time = 0


    def update(self, player_rect, other_enemies):
        super().update(player_rect, other_enemies)
        current_time = pygame.time.get_ticks()

        # Shooting logic
        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time
            return self.shoot(player_rect.centerx, player_rect.centery)


    def shoot(self, target_x, target_y):
        # Create a bullet aimed at the player
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y, (255, 0, 0), 10, 5,True)
        return new_bullet

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)