import random as rd
from colorama import Back, Style

class Board:
    def __init__(self, board_size):
            self.board_size = board_size + 2
            self.snake = []
            self.tail = []
            self.init_board()
        
    def create_plan(self):
        # Create a 12x12 board filled with empty '0'
        # and surrounded by walls 'W'
        board = [['W' if x == 0 or x == self.board_size - 1
                       or y == 0 or y == self.board_size - 1 
                   else 0 for x in range(self.board_size)] 
                  for y in range(self.board_size)]
        return board
    
    def init_board(self):
        # Reset the board to its initial state
        self.plan = self.create_plan()
        self.snake = []
        self.tail = []
        self.place_snake()
        self.place_buff()
        self.place_buff()
        self.place_debuff()
        self.direction = self.get_direction(self.snake[0], self.snake[1])

    def print_board(self):
        for row in self.plan:
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

    def place_snake(self):
        while True:
            head_x = rd.randint(1, self.board_size - 2)  # Avoid walls
            head_y = rd.randint(1, self.board_size - 2)
            head_pos = (head_y, head_x)

            # Check if the position is valid (not occupied by walls or body)
            if self.plan[head_y][head_x] == 0:
                # Place the head
                self.plan[head_y][head_x] = 'H'
                self.snake.insert(0, head_pos)

                # Place the body segments
                curr_pos = head_pos
                for _ in range(2):
                    valid_directions = self.get_adjacent_pos(curr_pos)
                    if valid_directions:
                        # Choose the first valid direction
                        direction = valid_directions[0]
                        dy, dx = direction

                        # Calculate the new position based on the direction
                        new_y, new_x = curr_pos[0] + dy, curr_pos[1] + dx

                        # Check if the new position is valid for the body
                        if self.plan[new_y][new_x] == 0:
                            self.plan[new_y][new_x] = 'S'

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
            if 1 <= ny < self.board_size and 1 <= nx < self.board_size and self.plan[ny][nx] == 0:
                valid_positions.append((dy, dx))

        return valid_positions
    
    def get_direction(self, head, neck):
        """
        Get the direction of the snake based on the head and neck positions.
        Returns a tuple (dy, dx).
        """
        y_diff = head[0] - neck[0]
        x_diff = head[1] - neck[1]

        return (y_diff, x_diff)

    def place_buff(self):
        # Place one buff randomly on the board
        while True:
            buff_x = rd.randint(0, self.board_size - 3)
            buff_y = rd.randint(0, self.board_size - 3)
            if self.plan[buff_x][buff_y] == 0:
                self.plan[buff_x][buff_y] = 'G'
                break
    
    def place_debuff(self):
        # Place one debuff randomly on the board
        while True:
            debuff_x = rd.randint(0, self.board_size - 3)
            debuff_y = rd.randint(0, self.board_size - 3)
            if self.plan[debuff_x][debuff_y] == 0:
                self.plan[debuff_x][debuff_y] = 'R'
                break