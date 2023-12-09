import pygame

from enemies.bullet import Bullet
from global_values import SCREEN_HEIGHT


class Player:
    def __init__(self, x, y, health=100):
        self.original_image = pygame.image.load('images/player.png').convert_alpha()  # Wczytanie tekstury gracza
        self.image = self.original_image  # Kopia oryginalnego obrazu
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4  # Określenie prędkości ruchu gracza
        self.health = health  # Określenie atrybutu życia

        # Ograniczenie przyjmowania obrażeń, raz na pół sekundy
        self.last_damage_time = 0
        self.damage_cooldown = 500
        self.damage = 20

        # Nowe atrybuty do skalowania
        self.scale_factor = 1.0  # Początkowy współczynnik skalowania

        self.damage_time = 0
        self.damage_effect_duration = 200  # Czas trwania efektu po otrzymaniu obrażeń w milisekundach
        self.max_alpha = 180  # Maksymalna przezroczystość efektu

        self.bullets_amount = 200

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
        bullets = []
        # Pobranie pozycji myszy
        target_x, target_y = pygame.mouse.get_pos()
        # Tworzenie pocisku
        for i in range(self.bullets_amount):
            if i % 2 == 0:
                bullets.append(Bullet(self.rect.centerx, self.rect.centery, target_x, target_y, (0, 0, 255), self.damage, 10, False, i*5))
            else:
                bullets.append(Bullet(self.rect.centerx, self.rect.centery, target_x, target_y, (0, 0, 255), self.damage, 10, False, -i*5))
        return bullets

    def take_damage(self, amount):
        self.damage_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time > self.damage_cooldown:
            self.health -= amount
            self.last_damage_time = current_time
            if self.health < 0:
                self.health = 0
            # ToDo Dodać ekran końcowy po śmierci

    def increase_damage(self, damage_increase=5):
        self.damage += damage_increase

    def increase_speed(self, speed_increase=0.3):
        if (self.speed < 10):
            self.speed += speed_increase

    def increase_size(self, scale_increment=-0.1):
        if (self.scale_factor > 0.99):
            self.scale_factor += scale_increment
            new_size = (int(self.original_image.get_width() * self.scale_factor),
                        int(self.original_image.get_height() * self.scale_factor))
            self.image = pygame.transform.scale(self.original_image, new_size)
            self.rect = self.image.get_rect(center=self.rect.center)

    def increase_bullets_amount(self):
        self.bullets_amount += 1