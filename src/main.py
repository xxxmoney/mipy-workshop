# Shadow Switch - v0.2: Tile-Based World
import pygame
import sys

# --- Constants ---
# Screen dimensions
WIDTH, HEIGHT = 800, 600
# Frames per second
FPS = 60
# Player properties
PLAYER_SIZE = 40
PLAYER_SPEED = 5
# Tile properties
TILESIZE = 40
GRID_WIDTH = WIDTH / TILESIZE
GRID_HEIGHT = HEIGHT / TILESIZE
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)  # Red
WALL_COLOR = (100, 100, 100)  # Grey
FLOOR_COLOR = (40, 40, 40)  # Dark Grey

# --- Map Data ---
# A simple hard-coded map. 'W' is a wall, '.' is a floor.
MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W..................W",
    "W.WWW..........WWW.W",
    "W...W..........W...W",
    "W.W.W..........W.W.W",
    "W...W..........W...W",
    "W.WWW..........WWW.W",
    "W..................W",
    "W..................W",
    "W.WWW..........WWW.W",
    "W...W..........W...W",
    "W.W.W..........W.W.W",
    "W...W..........W...W",
    "W.WWW..........WWW.W",
    "WWWWWWWWWWWWWWWWWWWW",
]


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    """Represents the player character."""

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)

    def update(self):
        """Update the player's position based on key presses."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # --- Boundary checks ---
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT


# --- Wall Class ---
class Wall(pygame.sprite.Sprite):
    """Represents a wall obstacle."""

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)


# --- Game Class ---
class Game:
    """Manages the game window, loop, and states."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shadow Switch")
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        """Starts a new game."""
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        # Iterate through the map data to create walls and find player start
        for row, tiles in enumerate(MAP):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    wall = Wall(self, col, row)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                elif tile == '.':
                    # Player starting position can be the first floor tile found
                    if not hasattr(self, 'player'):
                        self.player = Player(self, col, row)
                        self.all_sprites.add(self.player)

        # In case the map has no floor tiles, place player at a default spot
        if not hasattr(self, 'player'):
            self.player = Player(self, 1, 1)  # Default position
            self.all_sprites.add(self.player)

    def run(self):
        """The main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Handles all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        """Updates all sprite logic."""
        self.all_sprites.update()

    def draw(self):
        """Draws everything to the screen."""
        self.screen.fill(FLOOR_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        """Cleans up and exits the game."""
        self.running = False


# --- Main execution ---
if __name__ == '__main__':
    game = Game()
    game.new()  # Initialize a new game state
    while game.running:
        game.run()

    pygame.quit()
    sys.exit()

