from DataStructure.DoublyLinkedList import DoublyLinkedList
from collections import deque
from playsound import playsound
import random
import copy


class Game2048:
    def __init__(self, rows, cols):
        """
        Initialize the game board.
        :param rows: Number of rows in the game board.
        :param cols: Number of columns in the game board.
        """
        self.rows = rows
        self.cols = cols
        self.sparse_matrix = DoublyLinkedList()
        self.undo_stack = deque(maxlen=5)  # Stack to store previous states for undo
        self.redo_stack = []  # Stack to store states for redo
        self.biggest_number = 2048
        self.has_moved = False  #To control if the board moved or not
        self.generate_new_tile()
        self.generate_new_tile()

    def save_state(self, board=None):
        """
        Save the current state for undo/redo functionality.
        """
        if not board: board = copy.deepcopy(self.sparse_matrix)
        self.undo_stack.append(board)  # Add current state
        self.redo_stack = []  # Clear redo stack after a new move
        
    def generate_new_tile(self):
        """
        Add a new tile (2 or 4) to a random empty position on the board.
        """
        empty_positions = [(i, j) for i in range(self.rows)
                           for j in range(self.cols)
                           if self.sparse_matrix.get_node(i, j) is None]
        
        if empty_positions:
            i, j = random.choice(empty_positions)
            value = 4 if random.random() < 0.3 else 2
            self.sparse_matrix.add_node(value, i, j)

    def merge(self, node1, node2):
        """
        Merge node2 into node1 and delete node2.
        :param node1: The target node to merge into.
        :param node2: The node to be merged.
        """
        self.sparse_matrix.update_node(node1, node1.value + node2.value)
        self.sparse_matrix.delete_node(node2)

    # def to_left(self):
    #     """
    #     Shift all tiles to the left.
    #     """
    #     board_copy = copy.deepcopy(self.sparse_matrix)
    #     self.has_moved = False
    #     for i in range(self.rows):
    #         current = None
    #         the_most_left = 0
    #         for j in range(self.cols):
    #             node = self.sparse_matrix.get_node(i, j)
    #             if node:
    #                 if current is None: # == if (left side of node is wall)
    #                     current = node
    #                     if current.j != the_most_left:
    #                         self.has_moved = True
    #                     current.j = the_most_left
    #                 elif current.value == node.value:
    #                     self.merge(current, node)
    #                     self.has_moved = True
    #                     the_most_left = current.j + 1
    #                     current = None
    #                 else:
    #                     if node.j != current.j + 1:
    #                         self.has_moved = True
    #                     node.j = current.j + 1  #shift the node next to current
    #                     current = node  
    #     if self.has_moved:
    #         self.save_state(board_copy)
    #         self.after_move()
    #     else:
    #         return None

    # def to_right(self):
    #     """
    #     Shift all tiles to the right.
    #     """
    #     board_copy = copy.deepcopy(self.sparse_matrix)
    #     self.has_moved = False
    #     for i in range(self.rows):
    #         current = None
    #         the_most_right = self.cols - 1
    #         for j in range(self.cols - 1, -1, -1):  #NOTICE: range(start point, step len, break condition)
    #             node = self.sparse_matrix.get_node(i, j)
    #             if node:
    #                 if current is None:
    #                     current = node
    #                     if current.j != the_most_right:
    #                         self.has_moved = True
    #                     current.j = the_most_right
    #                 elif current.value == node.value:
    #                     self.merge(current, node)
    #                     self.has_moved = True
    #                     the_most_right = current.j - 1
    #                     current = None
    #                 else:
    #                     if node.j != current.j - 1:
    #                         self.has_moved = True
    #                     node.j = current.j - 1
    #                     current = node
    #     if self.has_moved:
    #         self.save_state(board_copy)
    #         self.after_move()
    #     else:
    #         return None

    # def to_up(self):
    #     """
    #     Shift all tiles up.
    #     """
    #     board_copy = copy.deepcopy(self.sparse_matrix)
    #     self.has_moved = False
    #     for j in range(self.cols):
    #         current = None
    #         the_most_up = 0
    #         for i in range(self.rows):
    #             node = self.sparse_matrix.get_node(i, j)
    #             if node:
    #                 if current is None:
    #                     current = node
    #                     if current.i != the_most_up:
    #                         self.has_moved = True
    #                     current.i = the_most_up
    #                 elif current.value == node.value:
    #                     self.merge(current, node)
    #                     self.has_moved = True
    #                     the_most_up = current.i + 1
    #                     i += 1
    #                     current = None
    #                 else:
    #                     if node.i != current.i + 1:
    #                         self.has_moved = True
    #                     node.i = current.i + 1
    #                     current = node
    #     if self.has_moved:
    #         self.save_state(board_copy)
    #         self.after_move()
    #     else:
    #         return None

    # def to_down(self):
    #     """
    #     Shift all tiles down.
    #     """
    #     board_copy = copy.deepcopy(self.sparse_matrix)
    #     self.has_moved = False
    #     for j in range(self.cols):
    #         current = None
    #         the_most_down = self.rows - 1
    #         for i in range(self.rows - 1, -1, -1):
    #             node = self.sparse_matrix.get_node(i, j)
    #             if node:
    #                 if current is None:
    #                     current = node
    #                     if current.i != the_most_down:
    #                         current.i = the_most_down
    #                 elif current.value == node.value:
    #                     self.merge(current, node)
    #                     self.has_moved = True
    #                     the_most_down = current.i - 1
    #                     i -= 1
    #                     current = None
    #                 else:
    #                     if node.i != current.i - 1:
    #                         self.has_moved = True
    #                     node.i = current.i - 1
    #                     current = node
                        
    #     if self.has_moved:
    #         self.save_state(board_copy)
    #         self.after_move()
    #     else:
    #         return None
    
    def shift_tiles(self, direction):
        """
        Shift all tiles in the given direction.
        Direction can be 'left', 'right', 'up', or 'down'.
        """
        board_copy = copy.deepcopy(self.sparse_matrix)
        self.has_moved = False

        
        if direction in ('left', 'right'):
            outer_loop_range = range(self.rows)
            inner_loop_range = range(self.cols) if direction == 'left' else range(self.cols - 1, -1, -1)
            
            get_node = lambda i, j: self.sparse_matrix.get_node(i, j)
            set_position = lambda node, pos: setattr(node, 'j', pos)
            frontier = lambda: 0 if direction == 'left' else self.cols - 1
            
            step = 1 if direction == 'left' else -1
        else:
            outer_loop_range = range(self.cols)
            inner_loop_range = range(self.rows) if direction == 'up' else range(self.rows - 1, -1, -1)
            
            get_node = lambda i, j: self.sparse_matrix.get_node(j, i)
            set_position = lambda node, pos: setattr(node, 'i', pos)
            frontier = lambda: 0 if direction == 'up' else self.rows - 1
            
            step = 1 if direction == 'up' else -1

        for outer_loop_index in outer_loop_range:
            current = None
            frontier_pos = frontier()
            for inner_loop_index in inner_loop_range:
                node = get_node(outer_loop_index, inner_loop_index)
                if node:
                    if current is None:
                        current = node
                        if (node.j if direction in ('left', 'right') else node.i) != frontier_pos:
                            self.has_moved = True
                        set_position(node, frontier_pos)
                    elif current.value == node.value:
                        self.merge(current, node)
                        self.has_moved = True
                        frontier_pos += step
                        current = None
                    else:
                        if (node.j if direction in ('left', 'right') else node.i) != frontier_pos + step:
                            self.has_moved = True
                        frontier_pos += step
                        set_position(node, frontier_pos)
                        current = node

        if self.has_moved:
            self.save_state(board_copy)
            self.after_move()
        else:
            playsound("Error.mp3")

    def to_left(self):
        """
        Shift all the tiles to left
        """
        self.shift_tiles('left')

    def to_right(self):
        """
        Shift all the tiles to right
        """
        self.shift_tiles('right')

    def to_up(self):
        """
        Shift all the tiles to up
        """
        self.shift_tiles('up')

    def to_down(self):
        """
        Shift all the tiles to down
        """
        self.shift_tiles('down')


    def check_game_over(self):
        """
        Check if there are no valid moves left (game over).
        """
        if self.sparse_matrix.size < self.rows * self.cols:
            return False  # There's still an empty cell
        
        for i in range(self.rows):
            for j in range(self.cols):
                node = self.sparse_matrix.get_node(i, j)
                if node:
                    # Check neighbors for possible merges
                    for delta_i, delta_j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        neighbor = self.sparse_matrix.get_node(i + delta_i, j + delta_j)
                        if neighbor and neighbor.value == node.value:
                            return False
        return True
    
    def check_win(self):
        for node in self.sparse_matrix:
            if node.value >= self.biggest_number:
                return True
        return False

    def after_move(self):
        """
        Perform operations after each move:
        - Add a new tile.
        """
        self.generate_new_tile()
        
    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(self.sparse_matrix))
            self.sparse_matrix = self.undo_stack.pop()
        else:
            print("Undo is no available: undo stack is empty")


    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.sparse_matrix)
            self.sparse_matrix = self.redo_stack.pop()
        else:
            print("Redo is no available: redo stack is empty")

    def __str__(self):
        board = [["[]" for _ in range(self.cols)] for _ in range(self.rows)] #create an empty board
        current = self.sparse_matrix.head
        while current:
            board[current.i][current.j] = str(current.value)
            current = current.next

        return "\n".join(["\t".join(row) for row in board])
    
    def run(self):
        """
        Run the game in an infinite loop, asking for user input to make moves.
        """
        while True:
            print(str(self))  # Display the current game board
            move = input("Enter your move (w = up, s = down, a = left, d = right, u = undo, r = redo q = quit): ").lower()
            
            if move == 'w':  # Move up
                self.to_up()
            elif move == 's':  # Move down
                self.to_down()
            elif move == 'a':  # Move left
                self.to_left()
            elif move == 'd':  # Move right
                self.to_right()
            elif move == 'u':  # Undo
                self.undo()
            elif move == 'r':  # Redo
                self.redo()
            elif move == 'q':  # Quit the game
                print("Thanks for playing!")
                break  # Exit the game loop
            else:
                print("Invalid move. Please use 'w', 'a', 's', 'd', or 'q'.")

            # Check if the game is over
            if self.check_game_over():
                print("GAME ENDED: Game Over! No more moves are possible.")
                break  # End the game if no valid moves are left

            # Check for win condition
            if self.check_win():
                print("GAME ENDED: Congratulations! You won!")
                break  # End the game if the player wins
                
                
                