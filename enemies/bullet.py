import pygame
import math
from global_values import SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet:
    def __init__(self, x, y, target_x, target_y, color, damage=20, speed=10, is_enemy_bullet=False, offset_angle=0):
        self.radius = max(5, damage // 4)  # Określenie promienia pocisku
        self.color = color  # Kolor niebieski
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)  # Utworzenie prostokąta wokół okręgu
        self.rect.center = (x, y)
        self.speed = speed

        self.damage = damage  # Ilość zadawanych obrażeń

        self.is_enemy_bullet = is_enemy_bullet

        self.offset_angle = offset_angle
        # Obliczanie wektora kierunkowego z uwzględnieniem przesunięcia kąta
        x_diff = target_x - x
        y_diff = target_y - y
        angle = math.atan2(y_diff, x_diff) + math.radians(self.offset_angle)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)

        # # Obliczanie wektora kierunkowego do celu
        # x_diff = target_x - x
        # y_diff = target_y - y
        # distance = (x_diff**2 + y_diff**2)**0.5  # Dystans euklidesowy
        # self.dx = x_diff / distance  # Składowa X wektora jednostkowego
        # self.dy = y_diff / distance  # Składowa Y wektora jednostkowego

    def update(self):
        # Ruch pocisku
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

    def did_bullet_hit_enemies(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                return True

        return False


    def did_bullet_hit_player(self, player_rect):
        # Additional logic for enemy bullets
        if self.is_enemy_bullet and self.rect.colliderect(player_rect):
            return True

        return False

    def did_bullet_left_view(self):
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)