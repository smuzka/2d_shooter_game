
import pygame
import sys
from player import Player


# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
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

    # Aktualizacja gracza
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)

    # Rysowanie powtarzającej się tekstury tła
    for y in range(0, SCREEN_HEIGHT, texture_rect.height):
        for x in range(0, SCREEN_WIDTH, texture_rect.width):
            screen.blit(ground_texture, (x, y))

    # Rysowanie gracza
    player.draw(screen)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Utrzymanie stałej liczby FPS
    clock.tick(MAX_FPS)