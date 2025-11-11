#  Dungeons and Starvation

## Repository
[Dungeons and Starvation Repository](https://github.com/naviclip/Final-Project)

## Description
My project will be a 32-bit game that features both traits of a visual novel and a time-based minigame with movement and 
action, concerning a man who has fallen deep into the dephths of a dungeon and must satisfy his humger as he makes his way towards an eventual camp.
This project is a piece of art that emphasizes on the importance of diligence and one's health.

## Features
- Title screen with start and quit button
	- It has the title logo, background and buttons to either start the game or quit and would most likely require functions having to do with GUI.
- Pause menu (resume, restart, back to title)
	- This feature can be linked to the ESC key so the program will receive the input and the user can pause the game any time and resume, restart or quit if desired. Will also work with GUI functions.
- End screen with button menu (restart, back to title)
	- This will show a "You win!"-type of scene at the end with a button for restarting the game or returning to the title menu.
- Visual Novel/Dialogue with character sprite
	- I can use pygame to load in the background image while having the character dialogue sprite blitted over the background with a textbox. The user can click through the dialogue by assigning the key to the left mouse button.
- Food position generator
	- I can first make the food objects and then predefine locations where the food (points that can fill up the hunger/health bar) is located (similar to a game level in earlier *Super Mario* games.
- Timed Gameplay
	- I can add a 60sec timer counting down to add a sense of urgency to the game that decreases with every frame. It will be displayed on the top left corner of the screen with the hunger bar for the player to see while playing.
- Platform system
	- I can create solid blocks in the air and on the ground that the player can stand on and cannot pass without going over or under them. This is to add an environment for the character to traverse on and a challenge with obstacles so the player is encouraged to work for the food the character requires. There should also be gravity implemented so the character does not float.
- Moving background
	- The background and obstacles will move based on the direction the player goes.
- Hunger/health bar system
	- The hunger bar shows how hungry the character is. The bar will have a value of 0-100. Every two seconds the character goes without food, the bar will automatically deplete by 10. The hunger bar will increase when the character collects food. If it is completely depleted, the game is over and the screen will transition to the "You lose" screen with buttons providing the ability to restart or quit to the title menu.
- Sprite movement 
	- I can make the character sprite move using WASD while changing direction and loop through 4 animation frames for each direction. When the character is still, it can use an idle frame. I'd have to make the sprites and provide a folder with all of them in it and labeled correctly for each animation with functions that help tie the animations together and to their respective movements and keys.
- Sprite interaction with food 
	- When the character interacts with the piece of food, the hunger bar will increase by a value of 20. This requires collision detection when the character comes into contact with the food.
- Goal interaction
	- When the character comes into contact with the goal, the game will end and display a graphic with buttons for restarting or returning to the title menu.

## Challenges
- I would need to dive deeper into pygame and make use of its other capabilities for many of these features including the dialogue, hunger bar, player movement, etc.
- I would need to learn about GUI and how to make a title/pause/end screen with buttons for the user
- I would need to put a lot of time into creating the graphics and animations
- I would need to put time into map creation

## Outcomes
Ideal Outcome:
- A program that has a working title screen with the start and quit button where the start button takes you straight to the game and starts the dialogue before it allows you to move the character with the background moving according to the movements of the character (right or left). There would be a 60sec timer at the top and a hunger bar that decreases every two seconds the character does not interact with food. The character can interact with the food, which increases the hunger/health bar, and can also run and jump on floating/sitting platforms. At the end of the dungeon, there will be a goal, where, once interacted with, will set off the "You win!" screen with buttons for restarting or returning to the title screen. Otherwise, if the timer runs out or if the hunger bar depletes, the "You lose!" screen will be triggered with buttons for restarting or returning to the title screen.

Minimal Viable Outcome:
- A program that has a working title screen with the start button that takes you straight to the game allows you to move the character with the background moving according to the movements of the character (right or left). There would be a 60sec timer at the top. The character can interact with the food, which increases the hunger/health bar, and can also run and jump on floating/sitting platforms. At the end of the dungeon, there will be a goal, where, once interacted with, will set off the "You win!" screen. Otherwise, if the timer runs out, the "You lose!" screen will be triggered.

## Milestones

- Week 1
  1. Set up file and asset folders
  2. Implement the main game loop
  3. Create left, right and still character sprites, label correctly and store in folder
  4. Create background, label correctly and store in folder
  5. Implement WASD movement
  6. Create food sprite, label correctly and store in folder
  7. Implement game system with title screen, game, pause, and end

- Week 2
  1. Implement the hunger system
  2. Implement food class
  3. Implement countdown timer
  4. Add goal area trigger
  5. Create character portraits for dialogue

- Week 3
  1. Add real title screen with start and quit
  2. Add real pause menu with resume, restart and return to title screen
  3. Add real end screen with restart and return to title screen
  4. Add dialogue with textbpx display, character portrait and advance key

- Week 4 (Final)
  1. Build map layout with obstacles
  2. Playtest for bugs
  3. Add fade transition between scenes if time allows
  4. Create video demo
