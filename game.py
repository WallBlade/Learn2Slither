import sys
import pygame as pg
from agent import Agent
from board import Board
from state import get_state
from draw import draw_board, draw_score
from utils import get_new_direction, is_valid_move, get_reward

GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


class Game:
    def __init__(self, args):
        pg.init()
        self.args = args
        self.sessions = args.sessions
        self.speed = args.speed
        self.visual = args.visual
        self.learn = not args.dontlearn
        self.save_path = args.save
        self.load_path = args.load
        self.board = Board(args.board_size)
        self.agent = Agent(self.sessions, self.save_path)
        self.direction = self.board.direction
        self.clock = pg.time.Clock()
        self.running = True
        self.pause = False
        self.step = args.step_by_step
        self.waiting = self.step
        self.w = args.w
        self.score = 3
        self.max_length = 3
        self.average = self.score
        if self.visual == 'on':
            no_frame = pg.NOFRAME
            self.screen = pg.display.set_mode((self.w, self.w + 50), no_frame)
            self.font = pg.font.Font('font/PressStart2P-Regular.ttf', 12)

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
        new_dir = get_new_direction(action)
        if new_dir is None:
            return

        # Track direction
        self.direction = new_dir

        # Calculate new position
        head = snake[0]
        y, x = head
        target = (y + new_dir[0], x + new_dir[1])
        reward = get_reward(plan, target)

        # Validate move
        if is_valid_move(snake, target) and self.args.mode == 'human':
            return reward

        # Replace old head with body
        plan[y][x] = 'S'

        # Calculate new coordinates
        dy, dx = new_dir
        new_y, new_x = y + dy, x + dx

        # Handle collision and movement
        if self.handle_collision(plan, new_y, new_x, snake):
            self.update_snake_position(plan, snake, new_y, new_x)

        return reward

    def init_game(self):
        self.score = 3
        self.board.init_board()
        self.pause = False
        self.running = True

    def run_human_mode(self):
        self.init_game()
        while self.running:
            events = pg.event.get()
            self.handle_events(events, 0)

            draw_board(self.screen, self.board.plan, self.direction)
            draw_score(self.font, self.screen, self.score, self.max_length)

            pg.display.flip()
            self.dt = self.clock.tick(self.speed)

    def handle_events(self, events, _):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_p:
                    self.pause = True
                    self.step = True
                    print(f"{RED}Pause: {self.pause}...{RESET}")
                elif event.key == pg.K_SPACE:
                    self.waiting = False
                elif event.key == pg.K_r:
                    print(f"{GREEN}Resume...{RESET}")
                    self.step = False
                    self.waiting = False
                elif event.key == pg.K_s and self.args.mode == 'ai':
                    self.agent.save_model(f'models/{_}sess.json')
                elif event.key == pg.K_UP:
                    self.speed += 10
                elif event.key == pg.K_DOWN:
                    self.speed -= 10
                elif event.key == pg.K_LEFT:
                    self.speed -= 1
                elif event.key == pg.K_RIGHT:
                    self.speed += 1
                else:
                    self.move(event, self.board.snake, self.board.plan)

    def run_ai_mode(self):
        """AI game mode."""
        self.load_model_if_needed()
        if not self.learn:
            self.agent.epsilon = 0.01
            self.agent.exploit_only = True
        training_stats = self.run_training_sessions()
        self.save_model_if_needed()
        self.print_final_stats(training_stats)

    def load_model_if_needed(self):
        """Load model"""
        if self.load_path:
            self.agent.load_model(self.load_path)

    def save_model_if_needed(self):
        """Save model"""
        if self.save_path:
            self.agent.save_model(self.save_path)

    def run_training_sessions(self):
        """Run all training sessions and return statistics."""
        print(f"{BLUE}Training in progress...{RESET}")

        stats = {
            'total_score': 3,
            'max_length': self.max_length,
            'max_duration': 0
        }

        for session in range(self.sessions):
            session_stats = self.run_single_session(session)
            self.update_training_stats(stats, session_stats, session)
            stats['average'] = stats['total_score'] / self.sessions

        return stats

    def run_single_session(self, session):
        """Run a single training session."""
        self.init_game()
        session_stats = {'duration': 0}

        while self.running:
            session_stats['duration'] += 1

            if not self.handle_game_tick(session):
                break

        return session_stats

    def handle_game_tick(self, session):
        """Process a single game tick."""
        self.wait_for_step(session)

        return self.process_ai_move()

    def wait_for_step(self, session):
        """Wait for the space key to be pressed to proceed to the next step."""
        events = pg.event.get()
        if self.step:
            self.waiting = True
            while self.waiting:
                events = pg.event.get()
                self.update_display()
                self.handle_events(events, session)
                if not self.waiting:
                    break
        self.handle_events(events, session)

    def process_ai_move(self):
        """Process AI move and update game state."""
        # Get current state and AI action
        state = get_state(self.board.plan, self.board.snake, False)
        action = self.agent.take_action(state, self.direction)

        # Execute move
        reward = self.move(action, self.board.snake, self.board.plan)
        # self.board.print_board()

        # Update best score if needed
        if self.score > self.max_length:
            self.max_length = self.score

        if self.learn:
            # Update AI model
            new_state = get_state(self.board.plan, self.board.snake)
            self.agent.update_q_table(state, action, reward, new_state)

        # Handle visualization if enabled
        self.update_display()

        return True

    def update_display(self):
        """Update game display if visualization is enabled."""
        if self.visual == 'on':
            draw_board(self.screen, self.board.plan, self.direction)
            draw_score(self.font, self.screen, self.score,
                       self.max_length)
            pg.display.flip()
        self.dt = self.clock.tick(self.speed)

    def update_training_stats(self, stats, session_stats, session):
        """Update overall training statistics with session results."""
        if session != 0:
            stats['total_score'] += self.score
        stats['max_duration'] = max(stats['max_duration'],
                                    session_stats['duration'])

    def print_final_stats(self, stats):
        """Print final training statistics."""
        print(
            f"{GREEN}Game over, "
            f"max length = {self.max_length}, "
            f"average length = {stats['average']}, "
            f"max duration = {stats['max_duration']}"
            f"{RESET}"
        )

    def run_game(self):
        if self.args.mode == 'human':
            self.run_human_mode()
        else:
            self.run_ai_mode()
        pg.quit()
