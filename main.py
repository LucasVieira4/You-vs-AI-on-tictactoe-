import pygame, sys
from pygame.locals import *
import os
from button import Button

pygame.init()

# Create screen
width = 600
height = 800
min_width = 300
min_height = 400
max_height = 900

screen = pygame.display.set_mode((width, height), RESIZABLE)

# Define colors
text_color = (23, 23, 19)
line_color = (190, 188, 185)
background_color = (79, 76, 66)

# Divide screen in 48 squares, based on the initial height
square_side = height // 8

# Define fonts
font = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 2)

# Load and resize the button image
button_image = pygame.image.load("assets/button.png")

def play():
    # Set the window caption for the play screen
    pygame.display.set_caption("Play!")

    global width, height, screen, square_side, font

    screen.fill(background_color)
    draw_lines()

    rects = create_rects()

    while True:
        play_mouse_position = pygame.mouse.get_pos()
        screen.fill(background_color)
        draw_lines()
        rects = create_rects()

        # Create the back button for the play screen
        play_back = Button(image=pygame.transform.scale(button_image, (square_side * 8 // 3, square_side * 6 // 5)), 
                           x_position=(width // 2), y_position=(15 * square_side // 2),
                           text_imput="BACK", font=pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 4))
        play_back.update(screen)

        for event in pygame.event.get():
            # Click top right red "x"
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse click anywhere
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, attributes in rects.items(): # Name is the key, and attributes is the value, of each one of the 9 items in the dict
                    rect = attributes["rect"] # Attributes is the value, but it's a dict as well

            # Mouse up and button pressed
            if event.type == pygame.MOUSEBUTTONUP:
                if play_back.check(play_mouse_position):
                    main_menu()

            if event.type == VIDEORESIZE:
                # Calculate new dimensions maintaining aspect ratio
                new_width, new_height = maintain_ratio(event.w, event.h)

                # Update screen dimensions if they have changed
                if (new_width, new_height) != (width, height):
                    width, height = new_width, new_height
                    screen = pygame.display.set_mode((width, height), RESIZABLE)
                    square_side = height // 8  # Update square_side after resize
                    font = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 2)  # Update font size after resize
                    draw_lines()
                    rects = create_rects()

            # Prevent fullscreening
            if event.type == FULLSCREEN:
                pass

            # Prevent resizing beyond limit
            if event.type == KEYDOWN:
                if event.key == K_UP and event.mod & KMOD_META:  # Windows key + up arrow
                    pass
                elif event.key == K_LEFT and event.mod & KMOD_META:  # Windows key + left arrow
                    pass
                elif event.key == K_RIGHT and event.mod & KMOD_META:  # Windows key + right arrow
                    pass

        pygame.display.update()



def main_menu():
    # Set the window caption for the main menu
    pygame.display.set_caption("You vs. AI!")
    while True:
        global width, height, screen, square_side, font
        screen.fill(background_color)

        # Get mouse position
        menu_mouse_position = pygame.mouse.get_pos()
        
        # Place text in the page
        menu_text = font.render("YOU VS. AI!", True, text_color)
        menu_rect = menu_text.get_rect(center=(width // 2, 3 * square_side // 2))

        menu_text_2 = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 3).render("(on tictactoe)", True, line_color)
        menu_rect_2 = menu_text_2.get_rect(center=(width // 2, 2 * square_side))

        # Create buttons
        play_button = Button(image=pygame.transform.scale(button_image, (square_side * 9 // 2, square_side * 9 // 4)), 
                             x_position=(width // 2), y_position=(7 * square_side // 2),
                             text_imput="PLAY", font=font)
        quit_button = Button(image=pygame.transform.scale(button_image, (square_side * 9 // 2, square_side * 9 // 4)), 
                             x_position=(width // 2), y_position=(5 * square_side),
                             text_imput="QUIT", font=font)
        
        screen.blit(menu_text, menu_rect)
        screen.blit(menu_text_2, menu_rect_2)

        # Event Handlers
        for button in [play_button, quit_button]:
            button.update(screen)
        
        for event in pygame.event.get():
            
            # Top right corner red "x" is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Mouse clicks on something
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                if play_button.check(menu_mouse_position):
                    play()
                if quit_button.check(menu_mouse_position):
                    pygame.quit()
                    sys.exit()

            if event.type == VIDEORESIZE:
                # Calculate new dimensions maintaining aspect ratio
                new_width, new_height = maintain_ratio(event.w, event.h)

                # Update screen dimensions if they have changed
                if (new_width, new_height) != (width, height):
                    width, height = new_width, new_height
                    screen = pygame.display.set_mode((width, height), RESIZABLE)
                    square_side = height // 8  # Update square_side after resize
                    font = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 2)  # Update font size after resize

            # Prevent fullscreening
            if event.type == FULLSCREEN:
                pass

            # Prevent resizing beyond limit
            if event.type == KEYDOWN:
                if event.key == K_UP and event.mod & KMOD_META:  # Windows key + up arrow
                    pass
                elif event.key == K_LEFT and event.mod & KMOD_META:  # Windows key + left arrow
                    pass
                elif event.key == K_RIGHT and event.mod & KMOD_META:  # Windows key + right arrow
                    pass

        pygame.display.update()

# Function that calculates the 3:4 aspect ratio
def maintain_ratio(event_w, event_h):
    ratio = 3 / 4  # Width / Height

    # Calculate new dimensions maintaining the aspect ratio
    if event_w / event_h > ratio:
        new_width = event_w
        new_height = (event_w * 4) / 3
    else:
        new_height = event_h
        new_width = (event_h * 3) / 4

    # Ensure the new dimensions are above the minimum size
    if new_width < min_width:
        new_width = min_width
        new_height = (new_width * 4) / 3
    if new_height < min_height:
        new_height = min_height
        new_width = (min_height * 3) / 4

    # Ensure height is below maximum size
    if new_height > max_height:
        new_height = max_height
        new_width = (max_height * 3) / 4

    return int(new_width), int(new_height)


def draw_lines():
    y_value = square_side
    x_value = square_side * 2
    for i in range(1, 5):
        pygame.draw.line(screen, line_color, (0, y_value), (width, y_value), 4)
        y_value += 2 * square_side
    for i in range(1, 3):
        pygame.draw.line(screen, line_color, (x_value, square_side), (x_value, 7 * square_side), 4)
        x_value += 2 * square_side

# Create the board. A dict that has 9 values, the position and if clicked    
def create_rects():
    rect_side = 2 * square_side
    rects = {}
    for i in range(3):
        for j in range(3):
            rect_name = f"rect_{i * 3 + j + 1}"
            rect = pygame.Rect(j * rect_side, (square_side + i * rect_side), rect_side, rect_side)
            rects[rect_name] = {
                "rect": rect,
                "name": rect_name,
                "clicked": False,
                "player": ""
            }
    return rects


main_menu()
