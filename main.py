
import pygame
import sys
from const_values import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from bullet import Bullet
from zombie import Zombie

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D deadly shooter")

# Ustawienia FPS
MAX_FPS = 60
clock = pygame.time.Clock()

# Wczytywanie tekstury ziemi
ground_texture = pygame.image.load("images/ground_texture.jpg").convert()
texture_rect = ground_texture.get_rect()

# Tworzenie instancji gracza
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

# Lista pocisków
bullets = []

# Lista przeciwników
enemies = []
enemy_spawn_time = 0  # Licznik czasu do następnego pojawienia się przeciwnika


# Główna pętla gry
while True:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Tworzenie nowego pocisku, gdy gracz strzela
            bullets.append(player.shoot())

    # Aktualizacja gracza
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)

    # Rysowanie powtarzającej się tekstury tła
    for y in range(0, SCREEN_HEIGHT, texture_rect.height):
        for x in range(0, SCREEN_WIDTH, texture_rect.width):
            screen.blit(ground_texture, (x, y))

    # Rysowanie gracza
    player.draw(screen)

    # Rysowanie paska zdrowia
    player.draw_health_bar(screen)


    # Aktualizacja i rysowanie pocisków
    for bullet in bullets:
        if bullet.update(enemies):
            bullets.remove(bullet)  # Usuwanie pocisku, jeśli trafi przeciwnika
        else:
            bullet.draw(screen)

    # Tworzenie nowych przeciwników
    if pygame.time.get_ticks() > enemy_spawn_time:
        enemies.append(Zombie(SCREEN_WIDTH, SCREEN_HEIGHT))
        enemy_spawn_time = pygame.time.get_ticks() + 1000  # Ustaw interwał pojawiania się przeciwników (np. co 2000 ms)

    # Aktualizacja przeciwników
    for enemy in enemies:
        if enemy.update(player.rect):
            player.take_damage(enemy.damage)

        if enemy.is_dead:
            enemies.remove(enemy)
        else:
            enemy.draw(screen)


    # Obliczanie upływającego czasu
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Zamiana milisekund na sekundy

    # Rysowanie czasu
    time_text = font.render(str(seconds), True, (255, 255, 255))  # Biały kolor tekstu
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(time_text, time_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Utrzymanie stałej liczby FPS
    clock.tick(MAX_FPS)