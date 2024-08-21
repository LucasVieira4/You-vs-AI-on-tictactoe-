import pygame, sys
from pygame.locals import *
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

hu_player = "x"
ai_player = "o"


def main_menu():
    
    # Set the window caption for the main menu
    pygame.display.set_caption("You vs. AI!")

    global width, height, screen, square_side, font

    initialize_buttons()
    
    while True:
        
        screen.fill(background_color)

        # Get mouse position
        menu_mouse_position = pygame.mouse.get_pos()
        
        # Place text in the page
        menu_text = font.render("YOU VS. AI!", True, text_color)
        menu_rect = menu_text.get_rect(center=(width // 2, 3 * square_side // 2))

        menu_text_2 = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 3).render("(on tictactoe)", True, line_color)
        menu_rect_2 = menu_text_2.get_rect(center=(width // 2, 2 * square_side))
        
        screen.blit(menu_text, menu_rect)
        screen.blit(menu_text_2, menu_rect_2)
        
        play_button.update(screen)
        quit_button.update(screen)
        
        # Event handlers
        for event in pygame.event.get():
            
            if event.type == VIDEORESIZE:
                screen_resize(event)
            # Top right corner red "x" is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check(menu_mouse_position):
                    play()
                if quit_button.check(menu_mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play():
    
    # Set the window caption for the play screen
    pygame.display.set_caption("Play!")

    global width, height, screen, square_side, font, rects

    rects = create_rects()  # Create the rectangles once
    initialize_buttons()

    while True:
        play_mouse_position = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen_resize(event)  # Handle screen resizing

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.check(play_mouse_position):
                    main_menu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which rectangle was clicked, by checking the index of the list
                for index, rect in enumerate(rects):
                    if rect.collidepoint(play_mouse_position) and board[index] == "none":
                        # Store the information of who clicked
                        board[index] = hu_player

                        # Draw the X as immediate feedback
                        draw_x(rect)

                        # Check if there's a win
                        if check_winner(board, hu_player):
                            endgame("win")
                        # Check if there are no available spots
                        elif len(available_spots(board)) == 0:  
                            endgame("draw")

                        # Call the minimax and find the best move for the ai
                        ai_move = minimax(board, ai_player) 
                        # Get what index minimax returned and define the rect that should be played based in that index
                        ai_rect = rects[ai_move["index"]]
                        # Store the information of where the ai played
                        board[ai_move["index"]] = ai_player

                        # Draw the O as immediate feedback
                        draw_o(ai_rect)   
                        # Check if the player did not lose yet
                        if check_winner(board, ai_player):
                            endgame("loss")

        # Drawing, because screen gets refreshed every frame
        screen.fill(background_color)  # Clear screen with background color
        draw_lines()  # Draw static grid lines
        for index, rect in enumerate(rects):
            if board[index] == hu_player:  # Check if the move was made by "x"
                draw_x(rect)
            elif board[index] == ai_player:
                draw_o(rect)

        back_button.update(screen)  # Draws the back button

        pygame.display.update()


def endgame(result):

    pygame.display.set_caption("Endgame")
    initialize_buttons()
    
    while True:
        draw_mouse_position = pygame.mouse.get_pos()
        
        screen.fill(background_color)  # Clear screen with background color
        
        won_text = font.render("YOU WON :)", True, line_color)
        won_text_2 = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 3).render("CONGRATULATIONS!", True, line_color)
        won_rect = won_text.get_rect(center=(width // 2, 3 * square_side // 2))
        won_rect_2 = won_text_2.get_rect(center=(width // 2, 2 * square_side))

        draw_text = font.render("IT'S A DRAW :/", True, line_color)
        draw_text_2 = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 3).render("AT LEAST IT'S NOT A DEFEAT...", True, line_color)
        draw_rect = draw_text.get_rect(center=(width // 2, 3 * square_side // 2))
        draw_rect_2 = draw_text_2.get_rect(center=(width // 2, 2 * square_side))

        loss_text = font.render("YOU LOST :(", True, line_color)
        loss_text_2 = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 3).render("WHAT A PITY...", True, line_color)
        loss_rect = loss_text.get_rect(center=(width // 2, 3 * square_side // 2))
        loss_rect_2 = loss_text_2.get_rect(center=(width // 2, 2 * square_side))
        
        if result == "loss":
            screen.blit(loss_text, loss_rect)
            screen.blit(loss_text_2, loss_rect_2)
        
        elif result == "win":
            screen.blit(won_text, won_rect)
            screen.blit(won_text_2, won_rect_2)

        else:
            screen.blit(draw_text, draw_rect)
            screen.blit(draw_text_2, draw_rect_2)

        # Event handling
        for event in pygame.event.get():
            
            if event.type == VIDEORESIZE:
                screen_resize(event)  # Handle screen resizing

            # Top right corner red "x" is clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if again_button.check(draw_mouse_position):
                    play()
                if quit_button.check(draw_mouse_position):
                    pygame.quit()
                    sys.exit()
        
        quit_button.update(screen) # Draws quit button
        again_button.update(screen) # Draws try again button
        pygame.display.update()


def screen_resize(event):

    global width, height, square_side, font, rects

    new_width, new_height = maintain_ratio(event.w, event.h)

    if (new_width, new_height) != (width, height):
        width, height = new_width, new_height
        screen = pygame.display.set_mode((width, height), RESIZABLE)
        square_side = height // 8
        font = pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 2)

        # Update rects with new positions and sizes
        rect_side = 2 * square_side
        rects = [pygame.Rect(j * rect_side, (square_side + i * rect_side), rect_side, rect_side) for i in range(3) for j in range(3)]
        
        # Initialize buttons again after resize
        initialize_buttons()

        # Update button positions
        update_buttons_positions()

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


def initialize_buttons():
    global back_button, play_button, quit_button, again_button
    
    # Initialize buttons with size and position
    back_button = Button(image=pygame.transform.scale(button_image, (square_side * 8 // 3, square_side * 6 // 5)), 
                        x_position=(width // 2), y_position=(15 * square_side // 2),
                        text_input="BACK", font=pygame.font.Font("assets/JetBrainsMono-Regular.ttf", square_side // 4))
    
    play_button = Button(image=pygame.transform.scale(button_image, (square_side * 9 // 2, square_side * 9 // 4)), 
                        x_position=(width // 2), y_position=(7 * square_side // 2),
                        text_input="PLAY", font=font)
    
    quit_button = Button(image=pygame.transform.scale(button_image, (square_side * 9 // 2, square_side * 9 // 4)), 
                        x_position=(width // 2), y_position=(5 * square_side),
                        text_input="QUIT", font=font)
    
    again_button = Button(image=pygame.transform.scale(button_image, (square_side * 13 // 2, square_side * 9 // 4)), 
                        x_position=(width // 2), y_position=(7 * square_side // 2),
                        text_input="TRY AGAIN?", font=font)


def update_buttons_positions():
    global back_button, play_button, quit_button, again_button
    
    back_button.x_position = width // 2
    back_button.y_position = 15 * square_side // 2
    back_button.rect.center = (back_button.x_position, back_button.y_position)
    back_button.text_rect.center = (back_button.x_position, back_button.y_position)

    play_button.x_position = width // 2
    play_button.y_position = 7 * square_side // 2
    play_button.rect.center = (play_button.x_position, play_button.y_position)
    play_button.text_rect.center = (play_button.x_position, play_button.y_position)

    quit_button.x_position = width // 2
    quit_button.y_position = 5 * square_side
    quit_button.rect.center = (quit_button.x_position, quit_button.y_position)
    quit_button.text_rect.center = (quit_button.x_position, quit_button.y_position)

    again_button.x_position = width // 2
    again_button.y_position = 7 * square_side // 2
    again_button.rect.center = (again_button.x_position, again_button.y_position)
    again_button.text_rect.center = (again_button.x_position, again_button.y_position)


def create_rects():
    global rects, board
    rect_side = 2 * square_side
    rects = [pygame.Rect(j * rect_side, (square_side + i * rect_side), rect_side, rect_side) for i in range(3) for j in range(3)]
    board = ["none"] * 9  # Initialize board with "none" for each cell
    return rects


def draw_lines():
    y_value = square_side
    x_value = square_side * 2
    for i in range(1, 5):
        pygame.draw.line(screen, line_color, (0, y_value), (width, y_value), 4)
        y_value += 2 * square_side
    for i in range(1, 3):
        pygame.draw.line(screen, line_color, (x_value, square_side), (x_value, 7 * square_side), 4)
        x_value += 2 * square_side


def draw_x(rect):
    pygame.draw.line(screen, line_color, ((rect.left + square_side / 3), (rect.top + square_side / 3)), ((rect.right - square_side / 3), (rect.bottom - square_side / 3)), int(square_side / 9))
    pygame.draw.line(screen, line_color, ((rect.left + square_side / 3), (rect.bottom - square_side / 3)), ((rect.right - square_side / 3), (rect.top + square_side / 3)), int(square_side / 9))


def draw_o(rect):
    pygame.draw.circle(screen, line_color, rect.center, (square_side * 3 / 4), int(square_side / 13))


# Checks if a player has won the game
def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for combination in winning_combinations: # Iterate through all the lists in the combinations list
        win = True
        for index in combination: # Iterate through all the elements of the current list
            if board[index] != player: # Uses the element as index to the board list, that has all the information. If not True, the player did not won in that way
                win = False
                break
        if win:  # If win is still True after checking the combination
            return True
    return False # None of the list combinations has been found True


def available_spots(board_state):

    available = []
    for index, move in enumerate(board_state):
        if move == "none":
            available.append(index)
    return available


def minimax(new_board, player):
    
    # Get all the avaiable spots in the board
    spots_available = available_spots(new_board)

    # Base cases
    if check_winner(new_board, hu_player):
        return {'score': -10}
    elif check_winner(new_board, ai_player):
        return {'score': 10}
    elif len(spots_available) == 0:  # Check if there are no available spots
        return {'score': 0}
    
    moves = []
    
    # Loop through available spots
    for spot in spots_available:
        #  Create an dict for each and store the index of that spot
        move = {}
        move["index"] = spot
        # Set the empty spot to the current player
        new_board[spot] = player

        if player == ai_player:
            # Call minimax with the changed board
            result = minimax(new_board, hu_player)
            move["score"] = result["score"]

        else:
            # Call minimax with the changed board
            result = minimax(new_board, ai_player)
            move["score"] = result["score"]

        new_board[spot] = "none"
        moves.append(move)

    # Evaluate the best move in moves
    if player == ai_player: # Chose the move with the highest score
        best_score = -10000
        # Iterate through moves
        for index, move in enumerate(moves):
            # If a move has a higher score than best_score, store the move
            if move["score"] > best_score:
                best_score = move["score"]
                best_move = index
    
    else:
        best_score = 10000
        # Iterate through moves
        for index, move in enumerate(moves):
            # If a move has a lower score than best_score, store the move
            if move["score"] < best_score:
                best_score = move["score"]
                best_move = index

    return moves[best_move]


main_menu()