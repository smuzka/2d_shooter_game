import pygame

class Bullet:
    def __init__(self, x, y, target_x, target_y, color, damage=20, speed=10, is_enemy_bullet=False):
        self.radius = 5  # Określenie promienia pocisku
        self.color = color  # Kolor niebieski
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)  # Utworzenie prostokąta wokół okręgu
        self.rect.center = (x, y)
        self.speed = speed

        self.damage = damage  # Ilość zadawanych obrażeń

        self.is_enemy_bullet = is_enemy_bullet

        # self.image = pygame.Surface((10, 4))  # Rozmiar pocisku
        # self.image.fill(color)  # Kolor
        # self.rect = self.image.get_rect(center=(x, y))
        # self.speed = 10

        # Obliczanie wektora kierunkowego do celu
        x_diff = target_x - x
        y_diff = target_y - y
        distance = (x_diff**2 + y_diff**2)**0.5  # Dystans euklidesowy
        self.dx = x_diff / distance  # Składowa X wektora jednostkowego
        self.dy = y_diff / distance  # Składowa Y wektora jednostkowego

    def update(self, enemies, player_rect):
        # Ruch pocisku
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                return True  # Pocisk zniknie po trafieniu przeciwnika

        # Additional logic for enemy bullets
        if self.is_enemy_bullet and self.rect.colliderect(player_rect):
            return True

        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)