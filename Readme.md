# Shadow Switch

## Description
**Shadow Switch** is a 2D pixel art game built with Pygame.  
The player controls a character capable of switching between two realities – a bright world and a shadow world.  
Each world contains unique paths, obstacles, and collectible items.  
The goal is to collect all items while avoiding traps by strategically switching between worlds.

## Core Features (Mandatory Requirements)

- **Intro Screen**  
  A short animation or static image displaying the game title, automatically transitioning to the menu.

- **Main Menu + Play Button**  
  A basic menu with a working “Play” button.

- **Multiple Sprite Types**  
  Includes different sprites for the player, items, light-world obstacles, shadow-world obstacles, and background tiles.

- **Spritesheets and Tiles**  
  Uses 64x64 pixel spritesheets and tile-based levels. Switching worlds changes the active tile layer.

- **Animations**  
  Player walking animation, switch-world transition effects, and collectible item animations.

- **User Input Handling**  
  - Arrow keys or WASD to move  
  - Spacebar to switch between worlds

- **Collision and Reactions**  
  Collisions depend on which world is currently active. Obstacles in the inactive world are ignored.

- **Score System**  
  Each collected item increases the score. The current score is always displayed on screen.

## Optional Features (if time allows)

- Basic sound effects (switching, collecting, collision)
- World-specific background music

## Why This Idea?

- The concept is original and not on the list of forbidden game types.
- It allows for visually interesting and mechanically engaging level design.
- It fully satisfies the assignment’s technical requirements.
- It’s well-suited for a two-person team.

## Technologies Used

- Python 3
- [Pygame] (https://www.pygame.org/)
- Numpy
