# **Shadow Switch \- Game Documentation**

## **1\. Game Design Specification**

### **1.1. Game Concept**

**"Shadow Switch"** is a top-down 2D puzzle game. The player controls a character who has the unique ability to switch between two parallel realities: the **Light World** and the **Shadow World**. The goal is to navigate through a series of levels by collecting all required items, avoiding traps, and solving environmental puzzles. Success hinges on the player's ability to strategically switch between the two worlds to overcome obstacles that are only present in one reality.

### **1.2. Core Mechanics**

#### **Player Movement**

* The player will be controlled using the standard WASD or Arrow Keys for movement in four directions (up, down, left, right).  
* Movement is tile-based, meaning the player moves from one grid square to the next.

#### **World Switching**

* The central mechanic of the game is switching between the Light and Shadow worlds. This will be triggered by pressing the Spacebar.  
* Each world has a different layout of obstacles. A path that is blocked by a wall in the Light World might be open in the Shadow World, and vice-versa.  
* **Technical Implementation**: We will represent each level with a single, two-layered map. Each tile on the map will have data for both its "Light" state and its "Shadow" state (e.g., 'wall' or 'floor'). The world-switching mechanic simply toggles which layer is currently active for collision and rendering.

#### **Collision Logic**

* The player's movement will be restricted by obstacles (e.g., walls).  
* Collision will only occur with obstacles that exist in the **currently active world**. This allows the player to "phase through" a Light World wall by switching to the Shadow World where the wall doesn't exist.

#### **Collectibles & Scoring**

* Each level will contain a number of collectible items.  
* The primary goal is to collect all of these items.  
* The player's score will be a count of the items collected. This score will be displayed on the UI at all times.  
* Collectibles exist independently of the worlds; they can be picked up in either reality. When the player collides with an item, it is collected and removed from the game.

### **1.3. Level Structure**

* Levels will be pre-designed and hard-coded into the game.  
* The design will focus on creating simple puzzles that require the player to think about which reality they need to be in to navigate the map and reach all the collectibles.  
* For example, a collectible might be surrounded by walls in the Light World, forcing the player to find an alternate path in the Shadow World to reach it.

### **1.4. Controls**

* **Move Up**: W / Up Arrow  
* **Move Down**: S / Down Arrow  
* **Move Left**: A / Left Arrow  
* **Move Right**: D / Right Arrow  
* **Switch World**: Spacebar

### **1.5. Art Style & Placeholders**

* Initially, all game elements (player, walls, collectibles) will be represented by simple colored squares (placeholders) to allow us to focus on mechanics.  
* The **Light World** will have a bright, clean aesthetic.  
* The **Shadow World** will have a dark, contrasting aesthetic.  
* These placeholders will be replaced by sprites from a spritesheet later in development.

## **2\. Core Components (v0.1)**

### **2.1. game.py \- Main File**

This file serves as the entry point for the game.

* **Constants**: Defines core game values like screen dimensions (WIDTH, HEIGHT), frame rate (FPS), and colors.  
* **Player Class**: A pygame.sprite.Sprite subclass. In this initial version, it's a simple red square that handles its own movement based on keyboard input.  
* **Game Class**: Manages the main game loop, window setup, event handling, and rendering.  
  * \_\_init\_\_(): Initializes Pygame, the screen, and creates sprite groups.  
  * run(): Contains the main while loop that drives the game.  
  * events(): Handles quitting the game.  
  * update(): Calls the .update() method on all sprites.  
  * draw(): Renders the background and all sprites.