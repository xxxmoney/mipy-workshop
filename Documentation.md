# **Shadow Switch \- Game Design Document**

### **1\. Game Concept**

**"Shadow Switch"** is a top-down 2D puzzle game. The player controls a character with the unique ability to switch between two parallel realities: the **Light World** and the **Shadow World**. The goal is to navigate through levels by collecting all required items and solving environmental puzzles that require switching between the worlds.

### **2\. Core Features & Mechanics**

#### **2.1. Game Flow**

1. **Intro Screen**: The game starts with a simple splash screen displaying the game's title. After a few seconds, it automatically transitions to the Main Menu.  
2. **Main Menu**: A central menu with a clickable "Play" button. Starting the game will lead to the main gameplay.  
3. **Gameplay**: The player navigates the level, switching between worlds to solve puzzles and collect items.

#### **2.2. Player Controls**

* **Movement**: WASD or Arrow Keys for top-down movement.  
* **World Switch**: Spacebar to instantly toggle between the Light and Shadow worlds.

#### **2.3. World Switching**

* The core mechanic. A path blocked in the Light World may be open in the Shadow World, and vice versa.  
* The level map is two-layered, and the game simply toggles which layer is active for collisions and visuals.

#### **2.4. Sprites & Environment**

* **Player**: The character controlled by the user.  
* **Obstacles**: Walls or traps that block the player's path in one of the two worlds.  
* **Collectibles**: Items scattered throughout the level. The goal is to collect all of them.  
* **Tiles**: The world is built from a tile-based map system.

#### **2.5. Collision & Interaction**

* The player will be blocked by obstacles that are solid in the currently active world.  
* When the player touches a collectible item, the item is removed, and the player's score increases.

#### **2.6. Scoring & UI**

* The game will display a score on-screen, which is a count of the collected items.

#### **2.7. Animation**

* **Player**: The player character will have a walking animation.  
* **World Switch**: A simple visual effect will play when the world is switched.  
* **Collectibles**: Items may have a simple animation (e.g., glowing or bobbing).