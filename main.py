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

# # Colors
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# Set up window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates a Surface
pygame.display.set_caption('Space Shooter')

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

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # Pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


# Game loop
def main():
    run = True
    fps = 60
    clock = pygame.time.Clock()
    level = 1
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)
    player_velocity = 5

    player = Player(300, 650)

    # Create a redraw function
    # It is created here so that it has access to local variables,
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
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(fps)
        redraw_window()

        # Check to see if the player has quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Get a dictionary of all keyboard keys.
        # Dictionary values are whether the key is pressed or not.
        # This allows us to look for multiple keys pressed at the same time.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0:  # Left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:  # Right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0:  # Up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() < HEIGHT:  # Down
            player.y += player_velocity


if __name__ == '__main__':
    main()
