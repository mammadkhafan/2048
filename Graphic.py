import pygame
import sys

class Game2048GUI:
    def __init__(self, game, window_width=600, window_height=600, margin_size=15):
        """
        Initialize the GUI for the 2048 game.
        :param game: An instance of the Game2048 class.
        :param window_width: Width of the game window.
        :param window_height: Height of the game window.
        """
        self.game = game
        self.window_width = window_width
        self.window_height = window_height
        self.margin_size = margin_size

        # Calculate dynamic tile size and margin        
        self.tile_size = min(
            (self.window_width - (game.cols + 1) * self.margin_size) // game.cols,
            (self.window_height - (game.rows + 1) * self.margin_size) // game.rows
        )

        # Adjust width and height based on calculated tile size
        self.width = self.tile_size * self.game.cols + self.margin_size * (self.game.cols + 1)
        self.height = self.tile_size * self.game.rows + self.margin_size * (self.game.rows + 1)

        self.colors = {
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),            
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
            "empty cells color": (189, 172, 151),
            "board color": (155, 137, 122),
            "end game overlay color": (255, 255, 255),
            "win text": (255, 215, 0),
            "game over text":  (225, 50, 50)
        }
        
        self.font = None
        self.screen = None
        self.error_sound = None
        self.game_over = False
        self.win = False
        self.end_game_layer_alpha = 0
        self.end_game_text_alpha = 0
        
    def initialize_pygame(self):
        """
        Initialize the Pygame environment.
        """
        pygame.init()
        pygame.mixer.init()
        self.error_sound = pygame.mixer.Sound('Error.mp3')
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2048")
        pygame.display.set_icon(pygame.image.load("2048_icon.png"))
        self.font = pygame.font.Font(None, int(self.tile_size // 2))

    def draw_tile(self, value, x, y):
        """
        Draw a single tile on the board.
        :param value: Value of the tile.
        :param x: X-coordinate of the tile.
        :param y: Y-coordinate of the tile.
        """
        rect_x = self.margin_size + (x * (self.tile_size + self.margin_size)) #cell size is tile_size + margin_size
        rect_y = self.margin_size + (y * (self.tile_size + self.margin_size))
        color = self.colors.get(value, self.colors["empty cells color"])  # Default color for empty tiles is board color
        
        pygame.draw.rect(self.screen, color, (rect_x, rect_y, self.tile_size, self.tile_size), border_radius=10)
        
        if value:
            text = self.font.render(str(value), True, (119, 110, 101))  #font render create a surface by a text
            text_rect = text.get_rect(center=(rect_x + self.tile_size // 2, rect_y + self.tile_size // 2)) #here I initialize were is the center
            self.screen.blit(text, text_rect) # text must add to the screen with the text_rect

    def draw_board(self):
        """
        Draw the entire game board.
        """
        self.screen.fill(self.colors["board color"])  # Background color
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                cell = self.game.sparse_matrix.get_node(i, j)
                value = cell.value if cell else None
                self.draw_tile(value, j, i) # j = x = column and i = y = row
        
        # If game is over or won, add the overlay and respective message
        if self.game_over:
            self.draw_fade_effect(False) # False = lose
        elif self.win:
            self.draw_fade_effect(True) # True = win

        pygame.display.flip()   #update the surface

    def keyEvent_handler(self, event):
        """
        Handle user input for game moves.
        :param event: Pygame event object.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.game.to_up()
            elif event.key == pygame.K_DOWN:
                self.game.to_down()
            elif event.key == pygame.K_LEFT:
                self.game.to_left()
            elif event.key == pygame.K_RIGHT:
                self.game.to_right()
            elif event.key == pygame.K_u:
                self.game.undo()
            elif event.key == pygame.K_r:
                self.game.redo()
                
    def draw_fade_effect(self, state: bool):
        """
        if you pass the state as True it means player has won
        else it means player has lost
        """
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill(self.colors["end game overlay color"])
        overlay.set_alpha(self.end_game_layer_alpha)
        self.screen.blit(overlay, (0, 0))   # width and height size is as same as surface's width and height
        
        text = "You Win!" if state else "Game Over"
        text_color = self.colors["win text"] if state else self.colors["game over text"]
        
        win_text = self.font.render(text, True, text_color)
        win_text.set_alpha(self.end_game_text_alpha)
        win_rect = win_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(win_text, win_rect)

    def run(self):
        """
        Run the GUI for the 2048 game.
        """
        self.initialize_pygame()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.game_over and not self.win:  # Only handle input if game is not over or won
                    self.keyEvent_handler(event)

            if self.game.check_game_over() and not self.game_over:
                self.game_over = True
                self.draw_board()
                pygame.time.delay(1000)  # Wait for 1 second before starting the fade effect

            # Check if the player has won (e.g., reached 2048)
            if self.game.check_win() and not self.win:
                self.win = True
                self.draw_board()
                pygame.time.delay(1000)  # Wait for 1 second before starting the fade effect

            if self.win or self.game_over:
                if self.end_game_layer_alpha < 150:
                    self.end_game_layer_alpha += 3
                elif self.end_game_text_alpha < 255:
                    self.end_game_text_alpha += 15

            self.draw_board()
            pygame.time.Clock().tick(30)  # Control the frame rate
