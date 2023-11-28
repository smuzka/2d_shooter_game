import pygame
import random
from abc import ABC, abstractmethod

class EnemyInterface(ABC):
    def __init__(self, screen_width, screen_height, health=100):
        self.health = health
        self.max_health = health

        self.is_dead = False

        self.rect = self.image.get_rect()

        # Losowe pojawianie się na brzegu ekranu
        if random.choice([True, False]):  # Losowe wybieranie między górnym/dolnym a lewym/prawym brzegiem
            self.rect.x = random.choice([0, screen_width - self.rect.width])
            self.rect.y = random.randint(0, screen_height - self.rect.height)
        else:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.choice([0, screen_height - self.rect.height])

        self.speed = 3  # Możesz dostosować prędkość przeciwnika

    @abstractmethod
    def update(self, player_rect):
        pass


    @abstractmethod
    def draw(self, screen):
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_dead = True  # Dodanie flagi wskazującej, że przeciwnik jest martwy

    def draw_health_bar(self, screen):
        # Rysowanie paska zdrowia nad przeciwnikiem
        health_bar_length = 50  # Długość paska zdrowia
        health_bar_height = 5  # Wysokość paska zdrowia
        fill = (self.health / self.max_health) * health_bar_length
        health_bar_outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, health_bar_length, health_bar_height)
        health_bar_fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10, fill, health_bar_height)
        pygame.draw.rect(screen, (255,0,0), health_bar_fill_rect)
        pygame.draw.rect(screen, (255,255,255), health_bar_outline_rect, 2)

    def resolve_collision(self, other):
        # Logika do rozwiązania kolizji
        if self.rect.x < other.rect.x:
            self.rect.x -= 1
        else:
            self.rect.x += 1

        if self.rect.y < other.rect.y:
            self.rect.y -= 1
        else:
            self.rect.y += 1