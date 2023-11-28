
import pygame
import sys

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
ground_texture = pygame.image.load("images/ground_texture.jpg").convert()  # Zamień "ground_texture.png" na ścieżkę do Twojego pliku z teksturą
texture_rect = ground_texture.get_rect()
# Główna pętla gry
while True:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rysowanie powtarzającej się tekstury tła
    for y in range(0, SCREEN_HEIGHT, texture_rect.height):
        for x in range(0, SCREEN_WIDTH, texture_rect.width):
            screen.blit(ground_texture, (x, y))
    # Aktualizacja ekranu
    pygame.display.flip()

    # Utrzymanie stałej liczby FPS
    clock.tick(MAX_FPS)