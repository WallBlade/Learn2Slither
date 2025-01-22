import pygame as pg
import random as rd

class Board:
    def __init__(self):
            # Create a 12x12 board filled with empty '0'
            # and surrounded by walls 'W'
            self.board_size = 12
            self.score_size = 50
            self.snake = []
            self.board = [['W' if x == 0 or x == self.board_size - 1
                           or y == 0 or y == self.board_size - 1 
                       else 0 for x in range(self.board_size)] 
                      for y in range(self.board_size)]
            self.place_snake()
            self.place_buff()
            self.place_buff()
            self.place_debuff()
            # for row_idx, row in enumerate(self.board):
            #     print(row)
        
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
    
    def draw(self, screen):
        # Draw the 10x10 board
        screen.fill('#CFE1BB')

        # Define the color map
        color_map = {
            0: '#B6C99B',
            'R': 'red',
            'G': 'green',
            'H': 'black',
            'S': 'black',
            'W': '#88986C',
        }
        rect_size = screen.get_width() / 12  # Size of each cell
        padding = 2  # Padding between cells

        # Draw the board
        for row_idx, row in enumerate(self.board):
            for col_idx, cell in enumerate(row):
                x = col_idx * rect_size + padding
                y = row_idx * rect_size + padding + self.score_size
                color = color_map.get(cell, 'white')  # Couleur de la case
                pg.draw.rect(screen, color, (x, y, rect_size - padding, rect_size - padding))
