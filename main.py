# Pygame Tutorial - Creating Space Invaders
# Tech With Tim
# https://www.youtube.com/watch?v=Q-__8Xw9KTM&t=1149s

import pygame
import os
import time
import random


# Initialize the font module
pygame.font.init()

# Window size
WIDTH = 750
HEIGHT = 750

# Set up window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates a Surface
pygame.display.set_caption('Space Shooter')

# Frame rate
FPS = 60

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

# Lasers
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

# Background
BACKGROUND_BLACK = pygame.image.load(os.path.join('assets', 'background-black.png'))
# Scale the background to fill the screen
BG = pygame.transform.scale(BACKGROUND_BLACK, (WIDTH, HEIGHT))


class Ship:
    COOLDOWN = FPS / 2  # 0.5 seconds

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img: pygame.Surface = None
        self.laser_img: pygame.Surface = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window: pygame.Surface):
        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
        # pygame.draw.rect(window, 'red', (self.x, self.y, 50, 50))  # Test rectangle
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def shoot(self):
        # Create a laser and add to list
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # Pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def move_lasers(self, velocity, objs: list):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs[:]:
                    if laser.collision(obj):
                        objs.remove(obj)
                        # The laser can only collide with one object
                        self.lasers.remove(laser)
                        break

    def health_bar(self, window):
        # Draw red rectangle
        pygame.draw.rect(
            window,
            'red',
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width(),
                10
            )
        )
        # Overlay with green rectangle
        pygame.draw.rect(
            window,
            'green',
            (
                # x, y, w, h
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width() * self.health / self.max_health,
                10
            )
        )


class Enemy(Ship):
    COLOR_MAP = {
        'red': (RED_SPACE_SHIP, RED_LASER),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        # Create a laser and add to list
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window: pygame.Surface):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not 0 <= self.y <= height

    def collision(self, obj):
        return collide(self, obj)


def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press SPACE to Start!", True, "white")
        WIN.blit(title_label, ((WIDTH - title_label.get_width()) / 2, (HEIGHT - title_label.get_height()) / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main()

    pygame.quit()


def collide(obj_1, obj_2):
    # Offset is the distance between objects, based on the top left coordinates
    offset_x = obj_2.x - obj_1.x
    offset_y = obj_2.y - obj_1.y
    # overlap() returns (x, y) coordinates of the point of pixel intersection
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) is not None


# Game loop
def main():
    run = True
    clock = pygame.time.Clock()
    level = 0
    lives = 7
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)

    player = Player(300, 630)
    player_velocity = 5
    lost = False
    lost_count = 0  # Used to display lost message for a time

    enemies = []
    wave_length = 0
    enemy_velocity = 0.5

    laser_velocity = 10

    # Create a redraw function
    # It is created inside main() so that it has access to local variables,
    #   and it can only be called from inside main()
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # Draw text
        # NOTE: CPython functions do not take keyword arguments - positional only
        level_label = main_font.render(
            f'Level: {level}',
            True,
            'white',
        )
        lives_label = main_font.render(
            f'Lives: {lives}',
            True,
            'white',
        )
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:  # Before player, so that you can always see the player icon
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_lable = lost_font.render('You Lost!', True, "white")
            WIN.blit(lost_lable, ((WIDTH - lost_lable.get_width()) / 2, (HEIGHT - lost_lable.get_height()) / 2))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        # Check to see if the player has quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Show the lost message
        if lost:
            lost_count += 1
            if lost_count > FPS * 3:  # 3 seconds
                run = False
            else:
                continue

        # Increase the level
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # Spawn enemies (off screen)
            for i in range(wave_length):
                enemy = Enemy(
                    x=random.randrange(50, WIDTH - 100),
                    y=random.randrange(-1500, -100),
                    color=random.choice(['red', 'blue', 'green'])
                )
                enemies.append(enemy)

        # Get a dictionary of all keyboard keys.
        # Dictionary values are whether the key is pressed or not.
        # This allows us to look for multiple keys pressed at the same time.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0:  # Left
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:  # Right
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:  # Up
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() + 20 < HEIGHT:  # Down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:  # Shoot laser
            player.shoot()

        # Move enemies and lasers
        for enemy in enemies[:]:  # enemies[:] creates a copy of the list
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            # Enemy shoots laser
            if random.randrange(0, 4 * FPS) == 1:
                enemy.shoot()

            # Check for collision with player
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            # Has enemy reached the bottom of the screen?
            elif enemy.y > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
                # Losing condition
                if lives <= 0:
                    lost = True

        # Move player lasers
        player.move_lasers(- laser_velocity, enemies)

        # Losing condition
        if player.health <= 0:
            lost = True


if __name__ == '__main__':
    main_menu()
