SCREEN_WIDTH = 1400
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Lista pocisków
bullets = []
enemy_bullets = []

trails = []

# Lista przeciwników
enemies = []
shooting_enemies = []
trail_enemies = []
enemy_spawn_time = 0  # Licznik czasu do następnego pojawienia się przeciwnika

# PowerUps
from enum import Enum
from powerUps.powerUpsGlobal import available_power_ups_names
from powerUps.powerUp import PowerUp
from powerUps.speedPowerUp import SpeedPowerUp
from powerUps.sizePowerUp import SizePowerUp
from powerUps.multiShotPowerUp import MultiShotPowerUp

available_power_ups = {
    available_power_ups_names['damage_up']: lambda x,y: PowerUp(x, y),
    available_power_ups_names['speed_up']: lambda x, y: SpeedPowerUp(x, y),
    available_power_ups_names['size_down']: lambda x, y: SizePowerUp(x, y),
    available_power_ups_names['multi_shot']: lambda x, y: MultiShotPowerUp(x, y),
}

available_power_ups_player_buff = {
    available_power_ups_names['damage_up']: lambda player: player.increase_damage(),
    available_power_ups_names['speed_up']: lambda player: player.increase_speed(),
    available_power_ups_names['size_down']: lambda player: player.increase_size(-0.2),
    available_power_ups_names['multi_shot']: lambda player: player.increase_bullets_amount(),
}

power_ups = []

# Stats
game_over = False
enemies_killed = 0
bullets_shot = 0