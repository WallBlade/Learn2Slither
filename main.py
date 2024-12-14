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
            self.get_adjacent_pos()
        
        def place_snake(self):
            # Place snake's head randomly on the board
            while True:
                head_x = rd.randint(0, self.board_size - 3)
                head_y = rd.randint(0, self.board_size - 3)
                if self.board[head_x][head_y] == 0:
                    self.board[head_x][head_y] = 'H'
                    break
        
        def place_body(self):
            body_x = 0
            
        def get_adjacent_pos(self):
            for row_idx, row in enumerate(self.board):
                for col_idx, col in enumerate(row):
                    if (self.board[row_idx][col_idx] == 'H'):
                        print(self.board[row_idx + 1][col_idx + 1])
            
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
                'W': 'orange',
            }
            rect_size = screen.get_width() / 10
            for row_idx, row in enumerate(self.board):
                for col_idx, cell in enumerate(row):
                    if (col_idx != 0 and col_idx != self.board_size - 1) and (row_idx != 0 and row_idx != self.board_size - 1):
                        x = col_idx * rect_size
                        y = row_idx * rect_size
                        color = color_map.get(cell)
                        pg.draw.rect(screen, color, (x, y, rect_size, rect_size), 1)

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