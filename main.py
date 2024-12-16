# Example file showing a circle moving on screen
import pygame as pg
import random as rd

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

class Game:
    # pygame setup
    pg.init()
    screen = pg.display.set_mode((720, 720))
    clock = pg.time.Clock()
    running = True
    dt = 0

    class Board:
        def __init__(self):
            # Create a 12x12 board filled with empty '0' and surrounded by walls 'W'
            self.board_size = 12
            self.board = [['W' if x == 0 or x == self.board_size - 1 or y == 0 or y == self.board_size - 1 
                       else 0 for x in range(self.board_size)] 
                      for y in range(self.board_size)]
            self.place_snake()
            self.place_buff()
            self.place_buff()
            self.place_debuff()
            for row_idx, row in enumerate(self.board):
                print(row)
        
        def place_snake(self):
            # Place snake's head randomly on the board
            while True:
                head_x = rd.randint(0, self.board_size - 3)
                head_y = rd.randint(0, self.board_size - 3)
                if self.board[head_x][head_y] == 0:
                    self.board[head_x][head_y] = 'H'
                    for _ in range(2):
                        x, y = head_x, head_y
                        valid_positions = self.get_adjacent_pos(x, y)
                        if valid_positions:
                            body_x, body_y = valid_positions[0]
                            self.board[body_x][body_y] = 'S'
                            x, y = body_x, body_y
                    break
            
        def get_adjacent_pos(self, x, y):
            """
            Find valid adjacent positions to place the body of the snake.
            Returns a list of valid coordinates (x, y).
            """
            # Possible relative directions: up, down, left, right
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            valid_positions = []

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                # Check if the position is within bounds and unoccupied
                if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
                    if self.board[new_x][new_y] == 0:
                        valid_positions.append((new_x, new_y))

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
            color_map = {
                0: 'white',
                'R': 'red',
                'G': 'green',
                'H': 'blue',
                'S': 'blue',
            }
            rect_size = screen.get_width() / 10
            for row_idx, row in enumerate(self.board):
                for col_idx, cell in enumerate(row):
                    if cell != 'W':
                        x = (col_idx - 1) * rect_size
                        y = (row_idx - 1) * rect_size
                        color = color_map.get(cell)
                        pg.draw.rect(screen, color, (x, y, rect_size, rect_size))

    board = Board()

    while running:
        # poll for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        keys = pg.key.get_pressed()
        if keys[pg.K_q] or keys[pg.K_ESCAPE]:
            running = False

        screen.fill("black")

        board.draw(screen)

        # flip() the display to put your work on screen
        pg.display.flip()

        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pg.quit()