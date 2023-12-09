
import pygame
import sys
import random
from global_values import SCREEN_WIDTH, SCREEN_HEIGHT, bullets, enemy_bullets, trails, enemies, shooting_enemies, trail_enemies, enemy_spawn_time, power_ups, available_power_ups_player_buff, game_over, enemies_killed, bullets_shot
from player import Player
from enemies.zombie import Zombie
from enemies.ranger import Ranger
from enemies.trailEnemy import TrailEnemy

# Inicjalizacja Pygame
pygame.init()
# Inicjalizacja modułu czcionek
pygame.font.init()
# Wybierz rozmiar czcionki
font = pygame.font.Font(None, 36)
info_font = pygame.font.Font(None, 24)

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
player.increase_size(2)

# Główna pętla gry
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Nowy pocisk
            if(not game_over):
                bullets_pack = player.shoot()
                for bullet in bullets_pack:
                    bullets_shot += 1
                    bullets.append(bullet)


    if player.health <= 0:
        game_over = True

        game_over_text = font.render("Gratulacje!!", True, (255, 255, 255))
        enemies_killed_text = font.render(f"Zabiłeś: {enemies_killed} wrogów", True, (255, 255, 255))
        bullets_fired_text = font.render(f"Wystrzeliłeś: {bullets_shot} pocisków", True, (255, 255, 255))

        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        enemies_killed_rect = enemies_killed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
        bullets_fired_rect = bullets_fired_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(game_over_text, text_rect)
        screen.blit(enemies_killed_text, enemies_killed_rect)
        screen.blit(bullets_fired_text, bullets_fired_rect)

    if game_over:
        pygame.display.flip()
        continue


    # Aktualizacja gracza
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)

    # Rysowanie powtarzającej się tekstury tła
    for y in range(0, SCREEN_HEIGHT, texture_rect.height):
        for x in range(0, SCREEN_WIDTH, texture_rect.width):
            screen.blit(ground_texture, (x, y))

    current_time = pygame.time.get_ticks()
    time_since_damage = current_time - player.damage_time
    if time_since_damage < player.damage_effect_duration:
        alpha = max(0, player.max_alpha - (player.max_alpha * (time_since_damage / player.damage_effect_duration)))
        damage_effect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        damage_effect.set_alpha(alpha)  # Ustaw zmienną przezroczystość
        damage_effect.fill((255, 0, 0))  # Czerwony kolor
        screen.blit(damage_effect, (0, 0))  # Nakładanie efektu na ekran

    # Obliczanie upływającego czasu
    total_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60


    # Usuwanie przeterminowanych śladów
    trails = [trail for trail in trails if not trail.is_expired(current_time)]

    # Rysowanie śladów
    for trail in trails:
        trail.draw(screen)
        if player.rect.colliderect(trail.rect):
            player.take_damage(5)  # Gracz otrzymuje obrażenia

    # Pociski gracza
    for bullet in bullets:
        bullet.update()
        if bullet.did_bullet_left_view():
            bullets.remove(bullet)
        elif bullet.did_bullet_hit_enemies(enemies + shooting_enemies + trail_enemies):
            bullets.remove(bullet)
        else:
            bullet.draw(screen)

    # Pociski przeciwników
    for bullet in enemy_bullets[:]:
        bullet.update()
        if bullet.did_bullet_left_view():
            enemy_bullets.remove(bullet)
        elif bullet.did_bullet_hit_player(player.rect):
            player.take_damage(bullet.damage)
            enemy_bullets.remove(bullet)
        else:
            bullet.draw(screen)

    # Tworzenie nowych przeciwników
    if pygame.time.get_ticks() > enemy_spawn_time:
        for i in range(max(5, seconds // 4)):
            random_number = random.random()
            if random_number < 0.5:
                enemies.append(Zombie(SCREEN_WIDTH, SCREEN_HEIGHT))
            elif random_number > 0.5 and random_number < 0.6:
                enemies.append(Zombie(SCREEN_WIDTH, SCREEN_HEIGHT, 1.5, 500, 100, 3))
            elif random_number > 0.6 and random_number < 0.7:
                shooting_enemies.append(Ranger(SCREEN_WIDTH, SCREEN_HEIGHT))
            elif random_number > 0.7 and random_number < 1:
                trail_enemies.append(TrailEnemy(SCREEN_WIDTH, SCREEN_HEIGHT, 2))

        enemy_spawn_time = pygame.time.get_ticks() + random.randrange(4000, 8000)

    # Aktualizacja przeciwników
    for enemy in enemies:
        enemy.update(player.rect, enemies)
        didEnemyTouchPlayer = enemy.did_touch_player(player.rect)
        if didEnemyTouchPlayer:
            player.take_damage(enemy.damage)
        if enemy.is_dead:
            enemies_killed += 1
            power_up = enemy.didDropPowerUp()
            if power_up:
                power_ups.append(power_up)
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
            enemies_killed += 1
            power_up = enemy.didDropPowerUp()
            if power_up:
                power_ups.append(power_up)
            shooting_enemies.remove(enemy)
        else:
            enemy.draw(screen)

    # Aktualizacja przeciwników zostawiających ślady
    for enemy in trail_enemies:
        enemy.update(player.rect, shooting_enemies)
        didEnemyTouchPlayer = enemy.did_touch_player(player.rect)
        if didEnemyTouchPlayer:
            player.take_damage(enemy.damage)
        if enemy.is_dead:
            enemies_killed += 1
            power_up = enemy.didDropPowerUp()
            if power_up:
                power_ups.append(power_up)
            trail_enemies.remove(enemy)
        else:
            enemy.draw(screen)
        trail = enemy.did_leave_trail(current_time)
        if trail:
            trails.append(trail)

    # Rysowanie i sprawdzanie zbierania power-upów
    for power_up in power_ups[:]:
        power_up.draw(screen)
        if player.rect.colliderect(power_up.rect):
            available_power_ups_player_buff[power_up.type](player)
            power_ups.remove(power_up)

    # Rysowanie gracza
    player.draw(screen)

    # Rysowanie paska zdrowia
    player.draw_health_bar(screen)

    # Rysowanie statystyk gracza
    damage_text = font.render(f"Obrażenia: {player.damage:.2f}", True, (255, 255, 255))
    speed_text = font.render(f"Szybkość: {player.speed:.2f}", True, (255, 255, 255))
    scale_text = font.render(f"Rozmiar: {player.scale_factor:.2f}", True, (255, 255, 255))
    screen.blit(damage_text, (10, 10))
    screen.blit(speed_text, (10, 35))
    screen.blit(scale_text, (10, 60))

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