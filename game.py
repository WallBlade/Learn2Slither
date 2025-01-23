# Example file showing a circle moving on screen
import pygame as pg
import random as rd
from agent import Agent
import sys

from board import Board

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

class Game:
    # pygame setup
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((600, 650), pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.selected_option = 0
        self.running = True
        self.pause = False
        self.font = pg.font.Font('font/PressStart2P-Regular.ttf', 16)
        self.dt = 0
        self.score = 0
        self.run_game()

    def get_direction(self, event, snake_dir):
        if event.key == pg.K_w:
            return (-1, 0)
        if event.key == pg.K_s:
            return (1, 0)
        if event.key == pg.K_a:
            return (0, -1)
        if event.key == pg.K_d:
            return (0, 1)
        if event.key == pg.K_q or event.key == pg.K_ESCAPE:
            self.pause = True
        return snake_dir

    def move(self, snake_dir, snake, plan, board):
        head = snake[0]
        y, x = head
        dy, dx = snake_dir
        new_y, new_x = y + dy, x + dx

        # Check if the new position is valid
        if plan[new_y][new_x] == 'W' or plan[new_y][new_x] == 'S':
            self.running = False
            return

        # Check if the new position is a buff or debuff
        # if plan[new_y][new_x] == 'G' or plan[new_y][new_x] == 'R':
        #     self.handle_collision(plan[new_y][new_x], snake, plan, snake[-1], board)

        # Update the snake's position
        plan[new_y][new_x] = 'H'
        snake.insert(0, (new_y, new_x))

        # Update the tail position
        tail = snake.pop()
        plan[tail[0]][tail[1]] = 0

    def handle_collision(self, cell, snake, plan, tail, board):
        """
        Handles collisions based on the cell type.
        """
        if cell == 'R':
            if len(snake) == 1:
                self.running = False
                return
            else:
                plan[tail[0]][tail[1]] = 0
                snake.pop()
                tail = snake[-1]
                board.place_debuff()
                self.score -= 1
        elif cell == 'G':
            board.place_buff()
            self.score += 1
            return
        plan[tail[0]][tail[1]] = 0
        snake.pop()

    def draw_menu(self, events):
        # Define menu options
        menu_options = ['Resume', 'Restart', 'Quit']
        num_options = len(menu_options)

        # Handle events for navigation
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.selected_option = (self.selected_option - 1) % num_options
                elif event.key == pg.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % num_options
                elif event.key == pg.K_RETURN:
                    if self.selected_option == 0:
                        self.pause = False
                    elif self.selected_option == 1:
                        self.reset_game()
                    elif self.selected_option == 2:
                        self.running = False

        self.screen.fill('#CFE1BB')

        for i, option in enumerate(menu_options):
            # Highlight the selected option
            if i == self.selected_option:
                color = '#738357'  # Selected
            else:
                color = '#000000'  # Unselected

            text = self.font.render(option, True, color)
            self.screen.blit(text, (100, 50 + i * 50))

        # Update the display
        pg.display.flip()
    
    def draw_score(self):
        """
        Render the score on the screen.
        """
        score_surface = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_surface, (10, 15))

    def reset_game(self):
        self.score = 0
        self.pause = False
        self.run_game()

    def get_vision(self, plan, y, x):
        rows, cols = len(plan), len(plan[0])

        # Print upward vision
        for i in range(y - 1, -1, -1):
            print(plan[i][x])

        # Print the row at the snake's position (left and right vision)
        print(plan[y])

        # Print downward vision
        for i in range(y + 1, rows):
            print(plan[i][x])

        print("----------------------------------------")

    def run_game(self):
        board = Board()
        plan = board.board
        snake = board.snake
        
        # Get valid directions for the snake's initial movement
        head = snake[0]
        valid_directions = board.get_adjacent_pos(head)
        
        # Pick a random valid direction
        snake_dir = rd.choice(valid_directions) if valid_directions else (0, 1)
        y, x = head
        
        while self.running:
            events = pg.event.get()

            if not self.pause:
                for event in events:
                    if event.type == pg.QUIT:
                        self.running = False
                    if event.type == pg.KEYDOWN:
                        snake_dir = self.get_direction(event, snake_dir)
                        self.move(snake_dir, snake, plan, board)
                        
                board.draw(self.screen)
                self.draw_score()
            else:
                self.draw_menu(events)

            pg.display.flip()
            self.dt = self.clock.tick(50) / 1000
    pg.quit()

def main():
    Game()

if __name__ == '__main__':
    main()