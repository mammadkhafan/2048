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

        # Dynamic tile size calculation
        self.tile_size = 100

        self.width = self.tile_size * self.game.cols + self.margin_size * (self.game.cols + 1)
        self.height = self.tile_size * self.game.rows + self.margin_size * (self.game.rows + 1)

        # Colors for tiles and text
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
            "score background": (25, 25, 25),
            "score text": (255, 255, 255),
            "end game overlay color": (255, 255, 255),
            "win text": (255, 215, 0),
            "game over text":  (225, 50, 50),
            "number colors": (119, 110, 101)
        }

        self.font = None
        self.screen = None
        self.error_sound = None
        self.game_over = False
        self.win = False
        self.end_game_layer_alpha = 0
        self.end_game_text_alpha = 0

        # Score attributes
        self.score_width = self.width // 3
        self.score_height = self.margin_size * 3
        self.high_score = 0
    
    def initialize_pygame(self):
        """
        Initialize the Pygame environment.
        """
        pygame.init()
        pygame.mixer.init()
        self.error_sound = pygame.mixer.Sound('Error.mp3')
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("2048")
        pygame.display.set_icon(pygame.image.load("2048_icon.png"))
        self.font = pygame.font.Font(None, int(self.tile_size // 2))
        self.update_offsets()

        # Calculate offsets to center the board
        self.offset_x = (self.window_width - self.width) // 2
        self.offset_y = (self.window_height - self.height) // 2

        self.font = pygame.font.Font(None, int(self.tile_size // 2))
        
    
    def draw_tile(self, value, x, y):
        """
        Draw a single tile on the board.
        :param value: Value of the tile.
        :param x: X-coordinate of the tile.
        :param y: Y-coordinate of the tile.
        """
        rect_x = self.offset_x + self.margin_size + (x * (self.tile_size + self.margin_size))
        rect_y = self.offset_y + self.margin_size + (y * (self.tile_size + self.margin_size))
        color = self.colors.get(value, self.colors["empty cells color"])  # Default color for empty tiles is board color

        pygame.draw.rect(self.screen, color, (rect_x, rect_y, self.tile_size, self.tile_size), border_radius=10)

        if value:
            text = self.font.render(str(value), True, self.colors["number colors"])
            text_rect = text.get_rect(center=(rect_x + self.tile_size // 2, rect_y + self.tile_size // 2))
            self.screen.blit(text, text_rect)
            
            
    def draw_score(self):
        """
        Draw the score section above the game board.
        """
        # Update high score
        self.high_score = max(self.high_score, self.game.player_score)

        # Background rectangle for the score
        score_rect = pygame.Rect(
            self.offset_x,
            self.offset_y - self.score_height - self.margin_size,
            self.width,
            self.score_height,
        )
        pygame.draw.rect(self.screen, self.colors["score background"], score_rect, border_radius=10)

        # Draw current score
        score_text = f"Score: {self.game.player_score}"
        score_surface = self.font.render(score_text, True, self.colors["score text"])
        score_rect = score_surface.get_rect(center=(self.offset_x + self.width // 4, self.offset_y - self.score_height // 2))
        self.screen.blit(score_surface, score_rect)

        # Draw high score
        high_score_text = f"High Score: {self.high_score}"
        high_score_surface = self.font.render(high_score_text, True, self.colors["score text"])
        high_score_rect = high_score_surface.get_rect(center=(self.offset_x + 3 * self.width // 4, self.offset_y - self.score_height // 2))
        self.screen.blit(high_score_surface, high_score_rect)
    
    def draw_board(self):
        """
        Draw the entire game board with the score.
        """
        self.screen.fill(self.colors["board color"])  # Background color

        # Draw score
        self.draw_score()

        # Draw tiles
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                cell = self.game.sparse_matrix.get_node(i, j)
                value = cell.value if cell else None
                self.draw_tile(value, j, i)  # j = x = column and i = y = row
                
        if self.game_over:
             self.draw_fade_effect(False) # False = lose
        elif self.win:
             self.draw_fade_effect(True) # True = win

        pygame.display.flip()  # Update the surface
        
        
    
    def update_offsets(self):
        """
        Update the offsets to center the game board within the window.
        """
        self.offset_x = (self.window_width - self.width) // 2
        self.offset_y = (self.window_height - self.height) // 2 + self.score_height



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
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.fill(self.colors["end game overlay color"])
        overlay.set_alpha(self.end_game_layer_alpha)
        self.screen.blit(overlay, (0, 0))   # width and height size is as same as surface's width and height
        
        text = "You Win!" if state else "Game Over"
        text_color = self.colors["win text"] if state else self.colors["game over text"]
        
        win_text = self.font.render(text, True, text_color)
        win_text.set_alpha(self.end_game_text_alpha)
        win_rect = win_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
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
                elif event.type == pygame.VIDEORESIZE:  # Window resize event
                    self.window_width, self.window_height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    self.update_offsets()  # Update board position
                    
                if not self.game_over and not self.win:  # Only handle input if game is not over or won
                    self.keyEvent_handler(event)

            if self.game.check_game_over() and not self.game_over:
                self.game_over = True
                self.draw_board()
                pygame.time.delay(1000)  # Wait for 1 second before starting the fade effect

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