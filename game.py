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
    def __init__(self, args):
        pg.init()
        self.args = args
        self.sessions = args.sessions
        self.speed = args.speed
        self.board = Board(args.board_size, args.w)
        self.clock = pg.time.Clock()
        self.running = True
        self.pause = False
        self.selected_option = 0
        self.dt = 0
        self.reward = 0
        self.score = 3
        self.best_score = 0
        self.average = self.score

    def get_new_direction(self, action):
        """Determine the new direction based on key press."""
        DIRECTIONS = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        if isinstance(action, int):
            return {
                0: DIRECTIONS['UP'],
                1: DIRECTIONS['DOWN'],
                2: DIRECTIONS['RIGHT'],
                3: DIRECTIONS['LEFT']
            }.get(action, None)

        if hasattr(action, 'key'):
            return {
                pg.K_w: DIRECTIONS['UP'],
                pg.K_s: DIRECTIONS['DOWN'],
                pg.K_d: DIRECTIONS['RIGHT'],
                pg.K_a: DIRECTIONS['LEFT']
            }.get(action.key, None)
        
        return None

    def is_valid_move(self, snake, new_target):
        """Check if the move is valid (not reversing into self)."""
        if len(snake) == 1:
            return
        return new_target == snake[1]

    def handle_collision(self, plan, new_y, new_x, snake):
        """Handle different types of collisions and board interactions."""
        # Wall or snake body collision
        if plan[new_y][new_x] == 'W' or plan[new_y][new_x] == 'S':
            self.running = False
            return False

        # Debuff collision
        if plan[new_y][new_x] == 'R':
            if len(snake) == 1:
                self.running = False
                return False
            else:
                tail = snake.pop()
                plan[tail[0]][tail[1]] = 0
                self.board.place_debuff()
                self.score -= 1

        # Buff collision
        if plan[new_y][new_x] == 'G':
            self.board.place_buff()
            self.score += 1
            return True

        # Regular move
        return True

    def update_snake_position(self, plan, snake, new_y, new_x):
        """Update snake position on the board."""
        # Remove tail if not growing
        if plan[new_y][new_x] != 'G':
            tail = snake.pop()
            plan[tail[0]][tail[1]] = 0

        # Update head position
        plan[new_y][new_x] = 'H'
        snake.insert(0, (new_y, new_x))

    def move(self, action, snake, plan):
        """Main move method coordinating snake movement."""
        # Get new direction
        new_dir = self.get_new_direction(action)
        if new_dir is None:
            return

        # Calculate new position
        head = snake[0]
        y, x = head
        target = (y + new_dir[0], x + new_dir[1])
        self.reward = self.get_reward(plan, target)

        # Validate move
        if self.is_valid_move(snake, target):
            return

        # Replace old head with body
        plan[y][x] = 'S'

        # Calculate new coordinates
        dy, dx = new_dir
        new_y, new_x = y + dy, x + dx

        # Handle collision and movement
        if self.handle_collision(plan, new_y, new_x, snake):
            self.update_snake_position(plan, snake, new_y, new_x)
    
    def get_reward(self, plan, target):
        """Calculate the reward for the current move."""
        if plan[target[0]][target[1]] == 'W' or plan[target[0]][target[1]] == 'S':
            return -10
        elif plan[target[0]][target[1]] == 'G':
            return 10
        elif plan[target[0]][target[1]] == 'R':
            return -5
        else:
            return -0.1
    
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
                        return
                    elif self.selected_option == 2:
                        self.running = False
                        pg.quit()
                        sys.exit()

        self.board.screen.fill('#CFE1BB')

        for i, option in enumerate(menu_options):
            # Highlight the selected option
            if i == self.selected_option:
                color = '#738357'  # Selected
            else:
                color = '#000000'  # Unselected

            text = self.board.font.render(option, True, color)
            self.board.screen.blit(text, (100, 50 + i * 50))

        # Update the display
        pg.display.flip()
    
    def draw_score(self):
        """
        Render the score on the screen.
        """
        score_surface = self.board.font.render(f"Score: {self.score} Best: {self.best_score} Average: {self.average:.2f}", True, (0, 0, 0))
        self.board.screen.blit(score_surface, (10, 15))
    
    def reset_game(self):
        self.score = 3
        self.board.init_board()
        self.pause = False
        self.running = True

    def run_human_mode(self):
        while self.running:
            events = pg.event.get()

            if not self.pause:
                for event in events:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                            self.pause = True
                        else:
                            self.move(event, self.board.snake, self.board.board)
                        print(f"Score: {self.score}")
                        self.board.print_board()    

                self.board.draw()
                self.draw_score()
            else:
                self.draw_menu(events)

            pg.display.flip()
            self.dt = self.clock.tick(self.speed)
    
    def run_ai_mode(self):
        agent = Agent()
        total_score = 3

        for _ in range(self.sessions):
            if not self.running:
                self.reset_game()
            while self.running:
                events = pg.event.get()

                if not self.pause:
                    for event in events:
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                                self.pause = True
                            elif event.key == pg.K_UP:
                                self.speed += 10
                            elif event.key == pg.K_DOWN:
                                self.speed -= 10
                    state = self.board.get_state()
                    # print(f"State: {state}")
                    # Get the next move from the agent
                    action = agent.take_action(state)

                    # Make the move
                    self.move(action, self.board.snake, self.board.board)
                    if self.score > self.best_score:
                        self.best_score = self.score
                    new_state = self.board.get_state()
                    agent.update_q_table(state, action, self.reward, new_state)
                    # print(f"Score: {self.score}")

                    # self.board.print_board()
                    self.board.draw()
                    self.draw_score()
                else:
                    self.draw_menu(events)

                pg.display.flip()
                self.dt = self.clock.tick(self.speed)
            if _ != 0:
                total_score += self.score
                self.average = total_score / _
            print(f"Score: {self.score}")
            print(f"iteration: {_}")
            print(f"Average: {self.average}")
        print(f"{GREEN}Training complete in {self.sessions}!")
        print(f"Best score: {self.best_score}")
        print(f"Average score: {self.average}{RESET}")
        pg.quit()

    def run_game(self):
        if self.args.mode == 'human':
            self.run_human_mode()
        else:
            self.run_ai_mode()