# Shadow Switch - v0.1: Basic Skeleton
import pygame
import sys

# --- Constants ---
# Screen dimensions
WIDTH, HEIGHT = 800, 600
# Frames per second
FPS = 60
# Player properties
PLAYER_SIZE = 50
PLAYER_SPEED = 5
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (255, 0, 0)  # Red for now


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    """
    Represents the player character.
    For now, it's just a colored square.
    """

    def __init__(self):
        super().__init__()
        # Create a placeholder image for the player
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(PLAYER_COLOR)
        # Get the rectangle object for positioning
        self.rect = self.image.get_rect()
        # Start the player in the center of the screen
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        """
        Update the player's position based on key presses.
        This method is called once per frame.
        """
        # Get a dictionary of all keys currently being held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # --- Boundary checks to keep the player on screen ---
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


# --- Game Class ---
class Game:
    """
    Main class to manage the game window, loop, and states.
    """

    def __init__(self):
        pygame.init()
        # Set up the screen and clock
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shadow Switch")
        self.clock = pygame.time.Clock()
        self.running = True

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

    def run(self):
        """The main game loop."""
        while self.running:
            # Keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            self.events()
            # Update game state
            self.update()
            # Draw everything
            self.draw()

    def events(self):
        """Handles all events, like closing the window."""
        for event in pygame.event.get():
            # Check for closing the window
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Updates all sprite logic."""
        self.all_sprites.update()

    def draw(self):
        """Draws everything to the screen."""
        # Fill the background with a solid color
        self.screen.fill(BLACK)
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        # After drawing everything, flip the display
        pygame.display.flip()

    def quit(self):
        """Cleans up and exits the game."""
        pygame.quit()
        sys.exit()


# --- Main execution ---
if __name__ == '__main__':
    game = Game()
    game.run()
    game.quit()
