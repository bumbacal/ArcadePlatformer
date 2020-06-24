# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
ENEMY_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
ENEMY_SCALING = 0.2

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 2
GRAVITY = 1
PLAYER_JUMP_SPEED = 16

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 350
RIGHT_VIEWPORT_MARGIN = 350
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# Player start position
PLAYER_START_X = 128 * TILE_SCALING * 2
PLAYER_START_Y = 128 * TILE_SCALING

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

ENEMY_MAIN_PATH = "images/zombies/"
