# You vs. AI! (on tictactoe)
#### Video Demo:  <URL HERE>
#### Description:
**A TicTacToe game against the computer, made with pygame.**

This is my final project for CS50.

## Project Structure

Inside of project file, you'll see the following folders and files:

```text
├── assets/
│   ├── button.png
│   └── JetBrainsMono-Regular.ttf
├── button.py
├── main.py
└──README.md
```

## 1. Assets:

The main file uses the font in the assets file throughout the project, and the button.png file is used to display the buttons used in the game on the screen. 

The font used is JetBrains Mono, which you can download on their own [website](https://www.jetbrains.com/lp/mono/).

The button image is used in the creation of the buttons, in the main file.

## 2. button.py:

The button.py file contains the definiton of a class, `'Button'`, which is used to create interactive buttons in the game. This class handles the rendering of buttons on the screen as well as detecting mouse interactions. 

I learned how to do this from a tutorial on YouTube. 

- **YouTube Video**: [HOW TO MAKE A MENU SCREEN IN PYGAME!](https://youtu.be/GMBqjxcKogA?si=BjeSlEWRd8I2usm1)
  > He talks about the button class after he's done with the menu, and helped me a lot in understanding how pygame works.

### Features:

- **Initialization:** The `Button` class is initialized with parameters such as an image, position (x and y coordinates), text input, and font. It automatically creates a rectangular area (`rect`) that matches the size of the button image.
  
- **Rendering:** The `update` method is responsible for drawing the button image and text onto the screen. It's used several times through main.py, always when I want to draw the button on the screen.
  
- **Interaction:** The `check` method detects if the mouse click occurred within the button's rectangular area. It's used on the event handling in the functions, checking if the mouse position when the click happened was within it's area.
  
## 3. main.py:

This is the main file of the game, where the functions that make the game work are defined and used. I won't explain the code line by line since it's pretty simple and readable, and I used a lot of comments that helped me write it and sure will help you understand it.

### Start:

The file starts importing some modules and the Button class from the button.py file. The most important thing where is `import pygame`, since this game is made with pygame. 

- The first thing is to start the pygame, with `pygame.init()`.

- Next, the screen is created using defined variables.
  
- The colors are defined next. I used 3 colors through this entire project.  
 1. text_color, `#171713`,
 2. line_color, `#bebcb9`;
 3. background_color, `#4f4c42`.

- Defined a variable called square_side, that is responsible for getting the height of the screen and dividing it by 8. It's useful so that I don't need to work with pixels; they seem like magical numbers to me. It's also useful when the screen is resized, since all that works with pixels and size can now just work with the resized size, making everything adjustable to any screen size.
  
- Defined the font and the button image as variables.
   
- Defined the human player to be `'x'` and the AI to be `'o'`.
---
### main_menu:

The menu is displayed as a function. It starts with a game loop, in which the screen is filled with the background color and it gets the mouse position with `menu_mouse_position = pygame.mouse.get_pos()`. 

Then, it creates the text and the rect (a Pygame object representing a rectangular area of the screen, used for positioning and collision detection) in with the text will be located and initiates the buttons:

```
screen.blit(menu_text, menu_rect)
screen.blit(menu_text_2, menu_rect_2)
play_button.update(screen)
quit_button.update(screen)
```
Then, we get to the event handling. It enters another loop, that says:
`for event in pygame.event.get():`.

It deals with 4 events:

1. Screen is resized. Calls the function [`screen_resize`](#screen_resize) to deal with it.
2. Top right corner red "x" is clicked. It closes the game and exit the program.
3. Play button is clicked. It runs [`play`](#play) function.
4. Quit button is clicked. Does the same as the top right "x".
   
After the events, it update the screen: `pygame.display.update()`.

---
### play:

When the play function is called, it creates the 9 rects of the board game. To do that, it calls the [`create_rects`](#create_rects) function. Then, to create the buttons on the screen, it calls the [`initialize_buttons`](#initialize_buttons) function.

The next step is to enter the game loop, in which we get the current mouse position and start the event handlers.

It deals with the same first 2 events of main_menu and adds the event of clicking on the back button. If it's clicked, we go back to the main menu by calling [`main_menu`](#main_menu).

Then, if the event is a click, it enters a loop that searches through the rects list (explained in the [`create_rects`](#create_rects) function) to check which rectangle was clicked, by checking the index of the list.

If the click is within the collide point of a rect and that rect wasn't clicked before, it updates (placing "x" in that spot) the board list, which represents the game board, a list of 9 elements that can be either "x", if clicked by the human, "o", if clicked by the AI, and "none", if not clicked yet.

After that, it calls [`draw_x`](#draw_x) and draws the X as immediate feedback to the click. Then, the loop checks if there's a win, by calling [`check_winner`](#check_winner). If there's a win, the [`endgame`](#endgame) function is called with "win" set as the parameter. If there isn't a win, it checks the length of the return value of [`available_spots`](#available_spots); if the length is 0, it means that there are no available spots; and if the game has not ended yet, it's a draw, so it calls the [`endgame`](#endgame) function with "draw" set as the parameter.

So, the human clilcked, and there's not a win or a draw; the AI gets to play. We use the [`minimax`](#minimax) function to find the best play for the AI and assign it to the variable "ai_move": `ai_move = minimax(board, ai_player) `

Then, get what index minimax returned and define the rect that should be played based on that index: `ai_rect = rects[ai_move["index"]]`, since minimax returns an index to the best move.

Next, store the information about where the AI played: `board[ai_move["index"]] = ai_player` and draws the "o" as immediate feedback, by calling the [`draw_o`](#draw_o) function on the rect.

The next step is to see if the AI has won the game with that move, calling the [`check_winner`](#check_winner) function again. If true, it calls the [`endgame`](#endgame) function with "loss" as it's parameter. If not, the loop ends, and we wait for the next input from the human.

Waiting the next input, since the screen gets refreshed every frame, screen is filled with the background color, again. 

After that, for the first time, the grid is drawn, by the function [`draw_lines`](#draw_lines). It seems that it should be earlier in the code, but the event handler loop only starts with a event, so, when the play button is clicked inside of main_menu and play() start running, this is one of the first things that happens.

Then, the board is checked and, for each "x" and "o" that is stored, each one is drawn in the screen, for each responsible function. Latter, as the last thing, the back button is drawn in the screen and the display gets updated.

---
### endgame:

The endgame function does the same as main_menu and play. Initializes the buttons, start the game loop, gets the mouse position and fills the screen with the background color, so all that was being displayed in the previous function/screen gets refreshed.
```
pygame.display.set_caption("Endgame")
initialize_buttons()

while True:
    won_mouse_position = pygame.mouse.get_pos()
    
    screen.fill(background_color)  # Clear screen with background color
```
Inside of the loop, we initialize all the possible text, for all the possible cases (and their respective rects).

Then, we check the parameter by which the function was called and and draw to the screen the respective text.

After that, we got the event handler part. It's almost the same. 
1. For each event, call [`screen_resize`](#screen_resize).
2. Check if the top right "x" was clicked;
3. Check if the try again button is clicked. If yes, call [`play`](#play).
4. Check if the quit button is clicked. Same results as clicking the top right "x".
   
After the loop, we draw the buttons to the screen and update it.

---
### screen_resize:

This function is called after the screen gets resized, and it calls [`maintain_ratio`](#maintain_ratio), that returns the ideal height and width and sets it as the new_height and new_width variables.

If the height and width are not the ones that they should be, based on the return value of [`maintain_ratio`](#maintain_ratio), we update the screen, redefining it with the new parameters, update the size of the 9 rects in the board, so that the clickable area changes with the screen, update the variable square_side, so all that uses it gets updated as well. Calls to [`update_buttons_positions`](#update_buttons_positions), that does what the name says.

This function basically updates everything that should be updated after the screen is resized.

___

### maintain_ratio:

It's a function that takes the current width and height as parameters and calculate what should be the ideal height and width based on the 3:4 aspect ratio, since the game runs on that scale. Then, it retuns them as ints.

---
### initialize_buttons:

This function creates all the button the game used at once. It uses the Button class that is defined in `button.py` and passes all the right parameters to it, including the button image, position, and text. So, after this function is called, we have all the buttons in different usable variables.

---
### update_buttons_positions:

This function updates the positions of all buttons on the screen after a resize event. It ensures that the buttons remain correctly aligned and proportioned based on the new screen dimensions.

---
### create_rects:

This function creates pygame rects inside of a double for loop, so that creating the 9 rectangles is faster. Every iteration, the right position of the rect is calculates based on the square_side and a variable called rect_size, which is the double of the previous one. All of the rects are created inside of a list called rects. After that, a list of 9 "none" elements is created, representing the board and the state of each rect, in that moment, not clicked.

---
### draw_lines:

This function is responsible for drawing the grid lines on the Tic Tac Toe board. It draws two vertical and two horizontal lines, dividing the screen into nine equal squares. The lines are drawn using the color defined in the line_color variable. To draw the lines, I used the `pygame.draw.line` function.

---
### draw_x:

Takes a rect from the rects list as a parameter and draws, with the same `pygame.draw.line` function, an "x" in the middle of it, using the line color.

---
### draw_o

Similar to draw_x, this function draws a "o" in the middle of the rect, using `pygame.draw.circle` function.

---
### check_winner:

This function sets all the possible board winning combination, including rows, columns and diagonals in a list. Then, checks the all the combinations in this list and compare to the board state -passed as a parameter, checking if any of the combinations with the player which was passed as a parameter could be found.

If yes, return True, else, return False.

---
### available_spots:

This function only goes throughout the list that was passed as a parameter to it. By checking the board, it can search for all the indexes that are still placed as "none", i.e. were not clicked.

For every "none", they are appended to the avaiable list. At the end of the loop, the list is returned. 

---
### minimax:
This is the most important function of the game, because it implements a decision-making algorithm that ensures the AI always plays optimally, making it unbeatable. The function evaluates all possible moves in the game to determine the best move for the AI, considering both its own and the player's potential moves.

This function returns an index of which of the rects should be played by the AI.

Since it's a very well known function and I didn't develop it myself, I will not explain it line by line.

It is a recursive functions, so, it has the base cases:

1. Returns +10 if the AI wins.
2. Returns -10 if the human wins.
3. Returns 0 if the game is a draw.

After, it loops through all the available spots, make a play and call minimax within that modified board. This way, it can iterate through all the possible plays the AI and the player can make. It stores the best score for each move and then return the best move for that board.

I learned how to create a minimax function with is tutorial from [FreeCodeCamp](https://www.freecodecamp.org/news/how-to-make-your-tic-tac-toe-game-unbeatable-by-using-the-minimax-algorithm-9d690bad4b37/). If you are interested in knowing how it works, take a look at the link.

### These were all the function from the main.py file, and now, you know all you can possible know about the game.

If you want to understand the game a little better, just take a look at the main,py file. In my view, it's pretty readable and i did a bunch of comments. Contact me if there's any doubt about the project.

---

## I loved taking CS50. I am Lucas and this is my project!
Thank you!
