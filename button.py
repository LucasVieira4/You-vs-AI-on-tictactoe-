text_color = (23, 23, 19)
line_color = (190, 188, 185)

class Button():
    def __init__(self, image, x_position, y_position, text_input, font):
        self.image = image
        self.x_position = x_position
        self.y_position = y_position
        self.rect = self.image.get_rect(center = (self.x_position, self.y_position))
        self.text_input = text_input
        self.text = font.render(self.text_input, True, line_color)
        self.text_rect = self.text.get_rect(center = (self.x_position, self.y_position))

    def update(self, screen):
        # Puts button image on the screen
        screen.blit(self.image, self.rect)
        # Puts text in screen
        screen.blit(self.text, self.text_rect)

    # Take a position and check if it's within the button borders
    def check(self, position):
        # Position is a tuple. [0] for x and [1] for y
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False