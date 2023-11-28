import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/player.png').convert_alpha()  # Wczytanie tekstury gracza
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # Możesz dostosować prędkość ruchu gracza

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