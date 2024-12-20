# Example file showing a circle moving on screen
import pygame as pg
import random as rd
import sys

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

class Game:
    # pygame setup
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((720, 720))
        self.clock = pg.time.Clock()
        self.running = True
        self.pause = False
        self.dt = 0
        self.run_game()

    class Board:
        def __init__(self):
            # Create a 12x12 board filled with empty '0'
            # and surrounded by walls 'W'
            self.board_size = 12
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
            color_map = {
                0: 'white',
                'R': 'red',
                'G': 'green',
                'H': 'blue',
                'S': 'blue',
            }
            rect = screen.get_width() / 10
            for row_idx, row in enumerate(self.board):
                for col_idx, cell in enumerate(row):
                    if cell != 'W':
                        x = (col_idx - 1) * rect
                        y = (row_idx - 1) * rect
                        color = color_map.get(cell)
                        pg.draw.rect(screen, color, (x, y, rect, rect))

    def move(self, event, snake_dir):
        if event.key == pg.K_w:
            return (-1, 0) if snake_dir != (1, 0) else snake_dir
        if event.key == pg.K_s:
            return (1, 0) if snake_dir != (-1, 0) else snake_dir
        if event.key == pg.K_a:
            return (0, -1) if snake_dir != (0, 1) else snake_dir
        if event.key == pg.K_d:
            return (0, 1) if snake_dir != (0, -1) else snake_dir
        if event.key == pg.K_q or event.key == pg.K_ESCAPE:
            self.pause = True
        return snake_dir

    def handle_collision(self, cell, snake, plan, tail, board):
        """
        Handles collisions based on the cell type.
        """
        if cell == 'R':
            if len(snake) == 1:
                self.running = False
            else:
                plan[tail[0]][tail[1]] = 0
                snake.pop()
                tail = snake[-1]
                board.place_debuff()
        elif cell == 'G':
            board.place_buff()
            return
        plan[tail[0]][tail[1]] = 0
        snake.pop()

    # def display_menu(self):


    def run_game(self):
        board = self.Board()
        plan = board.board
        snake = board.snake
        
        # Get valid directions for the snake's initial movement
        head = snake[0]
        valid_directions = board.get_adjacent_pos(head)
        
        # Pick a random valid direction
        snake_dir = rd.choice(valid_directions) if valid_directions else (0, 1)
        y, x = head
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    snake_dir = self.move(event, snake_dir)

            if not self.pause:
                plan[y][x] = 'S'
                y += snake_dir[0]
                x += snake_dir[1]
                tail = snake[-1]

                # Check for collision
                if plan[y][x] in ('W', 'S'):
                    self.running = False
                else:
                    tail = snake[-1]
                    self.handle_collision(plan[y][x], snake, plan, tail, board)
                    plan[y][x] = 'H'
                    snake.insert(0, (y, x))
            else:
                # self.display_menu()
                print('OKOK')

            board.draw(self.screen)

            pg.display.flip()
            self.dt = self.clock.tick(5) / 1000
    pg.quit()

def main():
    Game()

if __name__ == '__main__':
    main()