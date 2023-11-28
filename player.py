import pygame
from const_values import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, health=100):
        self.image = pygame.image.load('images/player.png').convert_alpha()  # Wczytanie tekstury gracza
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # Określenie prędkości ruchu gracza
        self.health = health  # Określenie atrybutu życia

    def update(self, keys_pressed):
        # Ruch gracza
        if keys_pressed[pygame.K_w]:  # W górę
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_s]:  # W dół
            self.rect.y += self.speed
        if keys_pressed[pygame.K_a]:  # W lewo
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_d]:  # W prawo
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        # Rysowanie paska zdrowia
        pygame.draw.rect(screen, (255, 0, 0), (10, SCREEN_HEIGHT - 30, self.health * 2, 20))
        pygame.draw.rect(screen, (255, 255, 255), (10, SCREEN_HEIGHT - 30, 200, 20), 2)