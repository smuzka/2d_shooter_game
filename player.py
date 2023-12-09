import pygame
from global_values import SCREEN_HEIGHT
from enemies.bullet import Bullet

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
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y, (0, 0, 255), self.damage)
        return bullet

    def take_damage(self, amount):
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
        self.speed += speed_increase

    def increase_size(self, scale_increment=-0.1):
        self.scale_factor += scale_increment
        new_size = (int(self.original_image.get_width() * self.scale_factor),
                    int(self.original_image.get_height() * self.scale_factor))
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(center=self.rect.center)  # Aktualizacja rect, aby zachować pozycję