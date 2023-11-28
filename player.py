import pygame
from const_values import SCREEN_WIDTH, SCREEN_HEIGHT
from bullet import Bullet

class Player:
    def __init__(self, x, y, health=100):
        self.image = pygame.image.load('images/player.png').convert_alpha()  # Wczytanie tekstury gracza
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5  # Określenie prędkości ruchu gracza
        self.health = health  # Określenie atrybutu życia

        # Ograniczenie przyjmowania obrażeń, raz na pół sekundy
        self.last_damage_time = 0
        self.damage_cooldown = 500

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

    def shoot(self):
        # Pobranie pozycji myszy
        target_x, target_y = pygame.mouse.get_pos()
        # Tworzenie pocisku
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y, (0, 0, 255))
        return bullet

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time > self.damage_cooldown:
            self.health -= amount
            self.last_damage_time = current_time
            if self.health < 0:
                self.health = 0
            # ToDo Dodać ekran końcowy po śmierci