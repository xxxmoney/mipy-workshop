# Shadow Switch - v0.4: Collectibles & Scoring
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
# Font
FONT_NAME = pygame.font.match_font('arial')

# --- Colors ---
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
COLLECTIBLE_COLOR = (255, 255, 0)  # Yellow
# Light World
LIGHT_WALL_COLOR = (130, 82, 1)
LIGHT_FLOOR_COLOR = (210, 180, 140)
# Shadow World
SHADOW_WALL_COLOR = (75, 0, 130)
SHADOW_FLOOR_COLOR = (48, 25, 52)

# --- Map Data ---
# 'W'=Wall, '.'=Floor, 'P'=Player, 'C'=Collectible
LIGHT_MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WP.C......W........W",
    "W.WWWWW...W...WWWW.W",
    "W...W.....W......W.W",
    "W.W.W.WWWWWWWWW..W.W",
    "W.W...W.......C..W.W",
    "W.W.WWWWW.WWWWWW.W.W",
    "W.W.W.......W....W.W",
    "W.W.W.WWWWWWW.WW.W.W",
    "W.W...W.......W..W.W",
    "W.WWWWW.WWWWWWWW.W.W",
    "W.C...W..........W.W",
    "W.WWWWW.WWWWWWWW.W.W",
    "W...............C..W",
    "WWWWWWWWWWWWWWWWWWWW",
]
SHADOW_MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WP.................W",
    "W.W.WWWWW.WWWWWWWW.W",
    "W.W...W.......W..W.W",
    "W.WWWWW.WWWWWWWW.W.W",
    "W................C.W",
    "W...WWWWWWWWWWWW...W",
    "W...........C......W",
    "W.WWWW...W...WWWWW.W",
    "W....W...W...W...W.W",
    "W.WW.W...W...W.WWW.W",
    "W.W....W...W...W.W.W",
    "W.WWWWWW...WWWWW.W.W",
    "W.C................W",
    "WWWWWWWWWWWWWWWWWWWW",
]
MAPS = {'light': LIGHT_MAP, 'shadow': SHADOW_MAP}


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def move(self, dx=0, dy=0):
        # We check for future collision based on movement delta
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
        self.move(dx=dx, dy=dy)
        self.rect.topleft = (self.x, self.y)


# --- Wall Class ---
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)


# --- Collectible Class ---
class Collectible(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE // 2, TILESIZE // 2))
        self.image.fill(COLLECTIBLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x * TILESIZE + TILESIZE // 2, y * TILESIZE + TILESIZE // 2)


# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shadow Switch")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_world = 'light'
        self.score = 0

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.load_world(self.current_world)
        self.run()

    def load_world(self, world_name):
        for wall in self.walls:
            wall.kill()

        # Clear collectibles ONLY if they are part of the world switch logic.
        # For this game, they persist between worlds, so we don't clear them.

        map_data = MAPS[world_name]
        wall_color = LIGHT_WALL_COLOR if world_name == 'light' else SHADOW_WALL_COLOR

        player_created = hasattr(self, 'player')

        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    wall = Wall(self, col, row, wall_color)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                elif tile == 'P' and not player_created:
                    self.player = Player(self, col, row)
                    self.all_sprites.add(self.player)
                elif tile == 'C' and not any(
                        c.rect.center == (col * TILESIZE + TILESIZE // 2, row * TILESIZE + TILESIZE // 2) for c in
                        self.collectibles):
                    collectible = Collectible(self, col, row)
                    self.all_sprites.add(collectible)
                    self.collectibles.add(collectible)

        if self.player:
            self.player.add(self.all_sprites)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.switch_world()

    def switch_world(self):
        if self.current_world == 'light':
            self.current_world = 'shadow'
        else:
            self.current_world = 'light'
        self.load_world(self.current_world)

    def update(self):
        self.all_sprites.update()
        # Check for player collision with collectibles
        # The 'True' argument removes the collectible sprite upon collision
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        if hits:
            self.score += 1

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        floor_color = LIGHT_FLOOR_COLOR if self.current_world == 'light' else SHADOW_FLOOR_COLOR
        self.screen.fill(floor_color)
        self.all_sprites.draw(self.screen)
        # Draw the score UI
        self.draw_text(f"Score: {self.score}", 30, WHITE, 10, 10)
        pygame.display.flip()

    def quit(self):
        self.running = False


# --- Main execution ---
if __name__ == '__main__':
    game = Game()
    while game.running:
        game.new()

    pygame.quit()
    sys.exit()
