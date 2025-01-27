import pygame as pg
import random as rd
import colorama
from colorama import Back, Style

class Board:
    def __init__(self, board_size=12, w=600, h=600):
            # Create a 12x12 board filled with empty '0'
            # and surrounded by walls 'W'
            self.board_size = board_size
            self.score_size = 50
            self.screen = pg.display.set_mode((w, h + self.score_size), pg.NOFRAME)
            self.font = pg.font.Font('font/PressStart2P-Regular.ttf', 16)
            self.snake = []
            self.tail = []
            self.init_board()
        
    def create_board(self):
        # Create a 12x12 board filled with empty '0'
        # and surrounded by walls 'W'
        board = [['W' if x == 0 or x == self.board_size - 1
                       or y == 0 or y == self.board_size - 1 
                   else 0 for x in range(self.board_size)] 
                  for y in range(self.board_size)]
        return board
    
    def init_board(self):
        # Reset the board to its initial state
        self.board = self.create_board()
        self.snake = []
        self.tail = []
        self.place_snake()
        self.place_buff()
        self.place_buff()
        self.place_debuff()

    def place_snake(self):
        # Place snake's head randomly on the board
        while True:
            head_x = rd.randint(1, self.board_size - 2)  # Avoid walls
            head_y = rd.randint(1, self.board_size - 2)
            head_pos = (head_y, head_x)

            # Check if the position is valid (not occupied by walls or body)
            if self.board[head_y][head_x] == 0:
                # Place the head
                self.board[head_y][head_x] = 'H'
                self.snake.insert(0, head_pos)

                # Place the body segments
                curr_pos = head_pos
                for _ in range(2):  # Two body segments
                    valid_directions = self.get_adjacent_pos(curr_pos)
                    if valid_directions:
                        # Choose the first valid direction
                        direction = valid_directions[0]
                        dy, dx = direction

                        # Calculate the new position based on the direction
                        new_y, new_x = curr_pos[0] + dy, curr_pos[1] + dx

                        # Check if the new position is valid for the body
                        if self.board[new_y][new_x] == 0:
                            self.board[new_y][new_x] = 'S'

                            # Update current position for the next segment
                            curr_pos = (new_y, new_x)
                            self.snake.append(curr_pos)
                            if _ == 1:
                                self.tail = curr_pos
                    else:
                        break
                break

    def get_adjacent_pos(self, pos):
        """
        Find valid adjacent positions.
        Returns a list of valid coordinates (x, y).
        """
        y, x = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        valid_positions = []

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 1 <= ny < self.board_size and 1 <= nx < self.board_size and self.board[ny][nx] == 0:
                valid_positions.append((dy, dx))

        return valid_positions
        
    def place_buff(self):
        # Place one buff randomly on the board
        while True:
            buff_x = rd.randint(0, self.board_size - 3)
            buff_y = rd.randint(0, self.board_size - 3)
            if self.board[buff_x][buff_y] == 0:
                self.board[buff_x][buff_y] = 'G'
                break
    
    def place_debuff(self):
        # Place one debuff randomly on the board
        while True:
            debuff_x = rd.randint(0, self.board_size - 3)
            debuff_y = rd.randint(0, self.board_size - 3)
            if self.board[debuff_x][debuff_y] == 0:
                self.board[debuff_x][debuff_y] = 'R'
                break
    
    def print_board(self):
        """
        Print the game board with colored representations
        
        Symbols:
        - 'W': Wall (White background)
        - 'H': Snake Head (Green background)
        - 'G': Buff (Yellow background)
        - 'R': Debuff (Red background)
        - 'S': Snake Body (Blue background)
        - 0: Empty space (Default)
        """
        for row in self.board:
            row_display = []
            for cell in row:
                if cell == 'W':
                    row_display.append(f"{Back.WHITE}  {Style.RESET_ALL}")
                elif cell == 'H':
                    row_display.append(f"{Back.GREEN}  {Style.RESET_ALL}")
                elif cell == 'G':
                    row_display.append(f"{Back.YELLOW}  {Style.RESET_ALL}")
                elif cell == 'R':
                    row_display.append(f"{Back.RED}  {Style.RESET_ALL}")
                elif cell == 'S':
                    row_display.append(f"{Back.BLUE}  {Style.RESET_ALL}")
                else:
                    row_display.append(f"{Back.BLACK}  {Style.RESET_ALL}")
            print(''.join(row_display))
        print('\n')
    
    def draw(self):
        # Draw the 10x10 board
        self.screen.fill('#CFE1BB')

        # Define the color map
        color_map = {
            0: '#B6C99B',
            'R': 'red',
            'G': 'green',
            'H': 'black',
            'S': 'black',
            'W': '#88986C',
        }
        rect_size = self.screen.get_width() / self.board_size  # Size of each cell

        # Draw the board
        for row_idx, row in enumerate(self.board):
            for col_idx, cell in enumerate(row):
                x = col_idx * rect_size
                y = row_idx * rect_size + self.score_size
                color = color_map.get(cell, 'white')  # Couleur de la case
                pg.draw.rect(self.screen, color, (x, y, rect_size, rect_size))
