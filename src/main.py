# Shadow Switch - v0.3: World Switching & Collision
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

# --- Colors ---
# General
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
# Light World
LIGHT_WALL_COLOR = (130, 82, 1)  # Brown
LIGHT_FLOOR_COLOR = (210, 180, 140)  # Tan
# Shadow World
SHADOW_WALL_COLOR = (75, 0, 130)  # Indigo
SHADOW_FLOOR_COLOR = (48, 25, 52)  # Dark Purple

# --- Map Data ---
# 'W' = Wall, '.' = Floor, 'P' = Player Start
LIGHT_MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WP........W........W",
    "W.WWWWW...W...WWWW.W",
    "W...W.....W......W.W",
    "W.W.W.WWWWWWWWW..W.W",
    "W.W...W..........W.W",
    "W.W.WWWWW.WWWWWW.W.W",
    "W.W.W.......W....W.W",
    "W.W.W.WWWWWWW.WW.W.W",
    "W.W...W.......W..W.W",
    "W.WWWWW.WWWWWWWW.W.W",
    "W.....W..........W.W",
    "W.WWWWW.WWWWWWWW.W.W",
    "W..................W",
    "WWWWWWWWWWWWWWWWWWWW",
]
SHADOW_MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WP.................W",
    "W.W.WWWWW.WWWWWWWW.W",
    "W.W...W.......W..W.W",
    "W.WWWWW.WWWWWWWW.W.W",
    "W..................W",
    "W...WWWWWWWWWWWW...W",
    "W..................W",
    "W.WWWW...W...WWWWW.W",
    "W....W...W...W...W.W",
    "W.WW.W...W...W.WWW.W",
    "W.W....W...W...W.W.W",
    "W.WWWWWW...WWWWW.W.W",
    "W..................W",
    "WWWWWWWWWWWWWWWWWWWW",
]
MAPS = {'light': LIGHT_MAP, 'shadow': SHADOW_MAP}


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    """Represents the player character."""

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def move(self, dx=0, dy=0):
        if not self.check_collision(dx, dy):
            self.x += dx
            self.y += dy

    def check_collision(self, dx=0, dy=0):
        # Create a temporary rect to check for future collision
        temp_rect = self.rect.copy()
        temp_rect.x += dx
        temp_rect.y += dy
        for wall in self.game.walls:
            if temp_rect.colliderect(wall.rect):
                return True
        return False

    def update(self):
        """Update the player's position based on key presses."""
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED

        # Move player if no collision
        self.move(dx=dx, dy=dy)
        self.rect.topleft = (self.x, self.y)


# --- Wall Class ---
class Wall(pygame.sprite.Sprite):
    """Represents a wall obstacle."""

    def __init__(self, game, x, y, color):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
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
        self.current_world = 'light'

    def new(self):
        """Starts a new game."""
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.load_world(self.current_world)

    def load_world(self, world_name):
        """Loads a map layout, clearing old walls and creating new ones."""
        # Clear existing walls
        for wall in self.walls:
            wall.kill()

        map_data = MAPS[world_name]
        wall_color = LIGHT_WALL_COLOR if world_name == 'light' else SHADOW_WALL_COLOR

        # Find player position and create walls
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    wall = Wall(self, col, row, wall_color)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                elif tile == 'P' and not hasattr(self, 'player'):
                    self.player = Player(self, col, row)
                    self.all_sprites.add(self.player)

        # Re-add player to ensure it's drawn on top
        if hasattr(self, 'player'):
            self.player.add(self.all_sprites)
        else:  # Default position if no 'P' in map
            self.player = Player(self, 1, 1)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.switch_world()

    def switch_world(self):
        """Switches between light and shadow worlds."""
        if self.current_world == 'light':
            self.current_world = 'shadow'
        else:
            self.current_world = 'light'
        self.load_world(self.current_world)

    def update(self):
        """Updates all sprite logic."""
        self.all_sprites.update()

    def draw(self):
        """Draws everything to the screen."""
        floor_color = LIGHT_FLOOR_COLOR if self.current_world == 'light' else SHADOW_FLOOR_COLOR
        self.screen.fill(floor_color)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        """Cleans up and exits the game."""
        self.running = False


# --- Main execution ---
if __name__ == '__main__':
    game = Game()
    game.new()
    while game.running:
        game.run()

    pygame.quit()
    sys.exit()
