
import pygame
import sys
import random
from global_values import SCREEN_WIDTH, SCREEN_HEIGHT, bullets, enemy_bullets, enemies, shooting_enemies, enemy_spawn_time
from player import Player
from enemies.zombie import Zombie
from enemies.ranger import Ranger

# Inicjalizacja Pygame
pygame.init()
# Inicjalizacja modułu czcionek
pygame.font.init()
# Wybierz rozmiar czcionki
font = pygame.font.Font(None, 36)
# Zapisanie czasu startu gry
start_ticks = pygame.time.get_ticks()

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
        if bullet.update(enemies + shooting_enemies, player):
            bullets.remove(bullet)  # Usuwanie pocisku, jeśli trafi przeciwnika
        else:
            bullet.draw(screen)

    # Pociski przeciwników
    for bullet in enemy_bullets[:]:
        if bullet.update(enemies, player.rect):
            player.take_damage(bullet.damage)
            enemy_bullets.remove(bullet)
        else:
            bullet.draw(screen)

    # Tworzenie nowych przeciwników
    if pygame.time.get_ticks() > enemy_spawn_time:
        if random.random() < 0.7:
            enemies.append(Zombie(SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            for i in range(5):
                shooting_enemies.append(Ranger(SCREEN_WIDTH, SCREEN_HEIGHT))
        enemy_spawn_time = pygame.time.get_ticks() + random.randrange(1000, 2000)  # interwał pojawiania się przeciwników

    # Aktualizacja przeciwników
    for enemy in enemies:
        enemy.update(player.rect, enemies)
        didEnemyTouchPlayer = enemy.did_touch_player(player.rect)
        if didEnemyTouchPlayer:
            player.take_damage(enemy.damage)
        if enemy.is_dead:
            enemies.remove(enemy)
        else:
            enemy.draw(screen)

    # Aktualizacja strzelających przeciwników
    for enemy in shooting_enemies:
        bullet = enemy.update(player.rect, shooting_enemies)
        if bullet:
            enemy_bullets.append(bullet)

        didEnemyTouchPlayer = enemy.did_touch_player(player.rect)
        if didEnemyTouchPlayer:
            player.take_damage(enemy.damage)
        if enemy.is_dead:
            shooting_enemies.remove(enemy)
        else:
            enemy.draw(screen)


    # Obliczanie upływającego czasu
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Zamiana milisekund na sekundy


    # Obliczanie upływającego czasu
    total_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    # Formatowanie czasu do formatu MM:SS
    time_str = "{:02d}:{:02d}".format(minutes, seconds)

    # Rysowanie czasu
    time_text = font.render(time_str, True, (255, 255, 255))  # Biały kolor tekstu
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(time_text, time_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Utrzymanie stałej liczby FPS
    clock.tick(MAX_FPS)