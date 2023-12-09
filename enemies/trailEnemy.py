import pygame
from enemies.enemy import EnemyInterface
from enemies.trail import Trail

class TrailEnemy(EnemyInterface):
    def __init__(self, screen_width, screen_height, speed=2, health=100, damage=10):
        self.original_image = pygame.image.load('images/trail_zombie.png').convert_alpha()
        self.image = self.original_image

        super().__init__(screen_width, screen_height, 100)

        self.health = health
        self.speed = speed
        self.damage = damage

        self.trail_cooldown = 100  # Co ile czasu zostawiany jest nowy ślad
        self.last_trail_time = 0


    def update(self, player_rect, other_enemies):
        super().update(player_rect, other_enemies)

    def did_leave_trail(self, current_time):
        if current_time - self.last_trail_time > self.trail_cooldown:
            self.last_trail_time = current_time
            return Trail(self.rect.x, self.rect.y, 20, 20, 5000)
        return None

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, self.rect)
