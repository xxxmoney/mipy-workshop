# Shadow Switch - v0.6: Multiple Levels
import pygame
import sys

# --- Constants ---
# Tile properties
TILESIZE = 64
# Screen dimensions
WIDTH = 12 * TILESIZE  # 768
HEIGHT = 10 * TILESIZE  # 640
# Frames per second
FPS = 60
# Player properties
PLAYER_SIZE = TILESIZE - 24
PLAYER_SPEED = 5
# Font
FONT_NAME = pygame.font.match_font('arial')

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)
COLLECTIBLE_COLOR = (255, 255, 0)
# Light World
LIGHT_WALL_COLOR = (130, 82, 1)
LIGHT_FLOOR_COLOR = (210, 180, 140)
# Shadow World
SHADOW_WALL_COLOR = (75, 0, 130)
SHADOW_FLOOR_COLOR = (48, 25, 52)

# --- Level Data ---
# We now have a list of levels. Each level is a dictionary
# containing the light and shadow map layouts.
LEVEL_1_LIGHT = [
    "WWWWWWWWWWWW",
    "WP.C...W...W",
    "W.WWWW.W.W.W",
    "W....W.W.W.W",
    "W.WW.W.W.W.W",
    "W.C..W...W.W",
    "W.WWWWWW.W.W",
    "W........W.W",
    "W....C...W.W",
    "WWWWWWWWWWWW",
]
LEVEL_1_SHADOW = [
    "WWWWWWWWWWWW",
    "WP.C.......W",
    "W.W.WWWWWW.W",
    "W.W........W",
    "W.WWWWWW.W.W",
    "W.C......W.W",
    "W.W.WWWW.W.W",
    "W.W.W....W.W",
    "W.W...C..W.W",
    "WWWWWWWWWWWW",
]
LEVEL_2_LIGHT = [
    "WWWWWWWWWWWW",
    "W.C......C.W",
    "W.WWWW.WWWWW",
    "WP.....W...W",
    "WWWWWW.W.C.W",
    "W........WWW",
    "W.WWWWWW...W",
    "W....C...W.W",
    "W.WWWWWW.W.W",
    "WWWWWWWWWWWW",
]
LEVEL_2_SHADOW = [
    "WWWWWWWWWWWW",
    "W.C......C.W",
    "W.W....W...W",
    "WP.WWWWW.W.W",
    "W....W.....W",
    "W.WW.W.WWWWW",
    "W.W..W.W...W",
    "W.W....W.C.W",
    "W.WWWWWW...W",
    "WWWWWWWWWWWW",
]
LEVELS = [
    {'light': LEVEL_1_LIGHT, 'shadow': LEVEL_1_SHADOW},
    {'light': LEVEL_2_LIGHT, 'shadow': LEVEL_2_SHADOW},
]


# --- Player Class (no changes) ---
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


# --- Wall Class (no changes) ---
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)


# --- Collectible Class (no changes) ---
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
        self.state = 'intro'
        self.current_level_index = 0

    def new_game(self):
        """Sets up all variables for the current level."""
        self.score = 0
        self.total_collectibles = 0
        self.current_world = 'light'
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.player = None
        self.load_level(self.current_level_index)

    def load_level(self, level_index):
        """Loads all assets for a specific level index."""
        level_data = LEVELS[level_index]
        self.total_collectibles = sum(row.count('C') for row in level_data['light'])

        for row, tiles in enumerate(level_data['light']):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)
                    self.all_sprites.add(self.player)
                elif tile == 'C':
                    collectible = Collectible(self, col, row)
                    self.all_sprites.add(collectible)
                    self.collectibles.add(collectible)

        self.load_world_layout(self.current_world)

    def load_world_layout(self, world_name):
        """Loads just the wall layout for the currently active world."""
        for wall in self.walls:
            wall.kill()

        map_data = LEVELS[self.current_level_index][world_name]
        wall_color = LIGHT_WALL_COLOR if world_name == 'light' else SHADOW_WALL_COLOR

        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    wall = Wall(self, col, row, wall_color)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)

        if self.player:
            self.player.add(self.all_sprites)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.switch_world()

    def switch_world(self):
        self.current_world = 'shadow' if self.current_world == 'light' else 'light'
        self.load_world_layout(self.current_world)

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        if hits:
            self.score += len(hits)
            # Check for win condition
            if self.score >= self.total_collectibles:
                self.next_level()

    def next_level(self):
        """Advances the game to the next level or to the win screen."""
        self.current_level_index += 1
        if self.current_level_index < len(LEVELS):
            self.new_game()  # Load the next level
        else:
            self.state = 'win'  # No more levels, go to win screen
            self.playing = False

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
        self.draw_text(f"Score: {self.score} / {self.total_collectibles}", 30, WHITE, 10, 10)
        self.draw_text(f"Level: {self.current_level_index + 1}", 30, WHITE, WIDTH - 10, 10, align="topright")
        pygame.display.flip()

    def show_intro_screen(self):
        start_time = pygame.time.get_ticks()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: waiting = False; self.running = False
                if event.type == pygame.KEYUP: waiting = False; self.state = 'menu'
            if pygame.time.get_ticks() - start_time > 3000: waiting = False; self.state = 'menu'
            self.screen.fill(BLACK)
            self.draw_text("Shadow Switch", 64, WHITE, WIDTH / 2, HEIGHT / 4, align="center")
            self.draw_text("Loading...", 22, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
            pygame.display.flip()

    def show_menu_screen(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            play_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 25, 200, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: waiting = False; self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and play_button.collidepoint(event.pos):
                    waiting = False
                    self.current_level_index = 0  # Reset to level 1 when playing from menu
                    self.state = 'playing'
            self.screen.fill(BLACK)
            self.draw_text("Shadow Switch", 64, WHITE, WIDTH / 2, HEIGHT / 4, align="center")
            pygame.draw.rect(self.screen, LIGHT_WALL_COLOR, play_button)
            self.draw_text("Play", 40, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
            pygame.display.flip()

    def show_win_screen(self):
        """Shows the final win screen."""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            menu_button = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2, 300, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: waiting = False; self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and menu_button.collidepoint(event.pos):
                    waiting = False
                    self.state = 'menu'  # Return to menu
            self.screen.fill(BLACK)
            self.draw_text("You Win!", 64, WHITE, WIDTH / 2, HEIGHT / 4, align="center")
            pygame.draw.rect(self.screen, SHADOW_WALL_COLOR, menu_button)
            self.draw_text("Back to Menu", 40, WHITE, WIDTH / 2, HEIGHT / 2 + 25, align="center")
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
        elif game.state == 'win':
            game.show_win_screen()

    pygame.quit()
    sys.exit()
