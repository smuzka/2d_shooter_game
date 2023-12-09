import pygame

class Trail:
    def __init__(self, x, y, width, height, duration):
        self.rect = pygame.Rect(x, y, width, height)
        self.duration = duration
        self.created_time = pygame.time.get_ticks()

    def draw(self, screen):
        trail_color = (0, 255, 0, 100)
        trail_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        trail_surface.fill(trail_color)
        screen.blit(trail_surface, self.rect.topleft)

    def is_expired(self, current_time):
        # Sprawdzenie, czy czas aktywności śladu minął
        return current_time - self.created_time > self.duration
