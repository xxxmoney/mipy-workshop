# Shadow Switch - v0.5.1: Game States & Flow Fix
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
BLACK = (0, 0, 0)
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
        if not self.check_collision(dx, dy):
            self.x += dx
            self.y += dy

    def check_collision(self, dx=0, dy=0):
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
        self.state = 'intro'  # Possible states: intro, menu, playing

    def new_game(self):
        """Sets up all variables for a new game."""
        self.score = 0
        self.current_world = 'light'
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.player = None  # Ensure player is reset
        self.load_world(self.current_world)

    def load_world(self, world_name):
        for wall in self.walls:
            wall.kill()

        map_data = MAPS[world_name]
        wall_color = LIGHT_WALL_COLOR if world_name == 'light' else SHADOW_WALL_COLOR

        player_created = self.player is not None

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
        """The main game loop for the 'playing' state."""
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Handles events for the 'playing' state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
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
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        if hits:
            self.score += len(hits)

    def draw_text(self, text, size, color, x, y, align="topleft"):
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        setattr(text_rect, align, (x, y))
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        floor_color = LIGHT_FLOOR_COLOR if self.current_world == 'light' else SHADOW_FLOOR_COLOR
        self.screen.fill(floor_color)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Score: {self.score}", 30, WHITE, 10, 10)
        pygame.display.flip()

    def show_intro_screen(self):
        """Displays the intro screen, waiting for key press or time out."""
        start_time = pygame.time.get_ticks()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                # Allow skipping intro with any key press
                if event.type == pygame.KEYUP:
                    waiting = False
                    self.state = 'menu'

            # Timeout after 3 seconds
            if pygame.time.get_ticks() - start_time > 3000:
                waiting = False
                self.state = 'menu'

            # Drawing
            self.screen.fill(BLACK)
            self.draw_text("Shadow Switch", 64, WHITE, WIDTH / 2, HEIGHT / 4, align="center")
            self.draw_text("Loading...", 22, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
            pygame.display.flip()

    def show_menu_screen(self):
        """Displays the main menu, waiting for the user to click 'Play'."""
        waiting = True
        while waiting:
            self.clock.tick(FPS)

            # Define button here to check for mouse hover later if needed
            play_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 25, 200, 50)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        waiting = False
                        self.state = 'playing'

            # Drawing
            self.screen.fill(BLACK)
            self.draw_text("Shadow Switch", 64, WHITE, WIDTH / 2, HEIGHT / 4, align="center")
            pygame.draw.rect(self.screen, LIGHT_WALL_COLOR, play_button)
            self.draw_text("Play", 40, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
            pygame.display.flip()


# --- Main execution ---
if __name__ == '__main__':
    game = Game()
    while game.running:
        if game.state == 'intro':
            game.show_intro_screen()
        elif game.state == 'menu':
            game.show_menu_screen()
        elif game.state == 'playing':
            game.new_game()
            game.run()

    pygame.quit()
    sys.exit()
