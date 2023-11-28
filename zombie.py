import pygame
from enemy import EnemyInterface

class Zombie(EnemyInterface):
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load('images/zombie.png').convert_alpha()
        super().__init__(screen_width, screen_height)

        self.speed = 2  # Prędkość
        self.damage = 10  # Ilość zadawanych obrażeń

    def update(self, player_rect):
        # Ruch w kierunku gracza
        x_diff = player_rect.x - self.rect.x
        y_diff = player_rect.y - self.rect.y
        distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
        if distance == 0:
            distance = 0.001
        dx = x_diff / distance
        dy = y_diff / distance

        self.rect.x += self.speed * dx
        self.rect.y += self.speed * dy

        # Wykrywanie kolizji z graczem
        if self.rect.colliderect(player_rect):
            return True  # Zwracanie wartości True, gdy nastąpi kolizja
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)  # Rysowanie paska zdrowia