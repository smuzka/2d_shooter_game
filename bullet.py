import pygame


class Bullet:
    def __init__(self, x, y, target_x, target_y, color):
        self.radius = 5  # Określenie promienia pocisku
        self.color = color  # Kolor niebieski
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)  # Utworzenie prostokąta wokół okręgu
        self.rect.center = (x, y)
        self.speed = 10

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


    def update(self):
        # Ruch pocisku
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)