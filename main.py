# Example file showing a circle moving on screen
import pygame as pg
import random as rd

class Game:
    # pygame setup
    pg.init()
    screen = pg.display.set_mode((720, 720))
    clock = pg.time.Clock()
    running = True
    dt = 0

    class Board:
        def __init__(self):
            # Create a 10x10 board filled with zeros
            self.board_size = 10
            self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
            self.place_snake()
        
        def place_snake(self):
            # Place the head of the snake randomly on the board
            head_x = rd.randint(0, self.board_size - 1)
            head_y = rd.randint(0, self.board_size - 1)
            self.board[head_x][head_y] = 'H'
        
        def draw(self, screen):
            # Draw the 10x10 board
            rect_size = screen.get_width() / 10
            for row_idx, row in enumerate(self.board):
                for col_idx, cell in enumerate(row):
                    x = col_idx * rect_size
                    y = row_idx * rect_size
                    color = "white" if cell == 0 else "blue" # Color depends on the cell value
                    pg.draw.rect(screen, color, (x, y, rect_size, rect_size), 5)

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