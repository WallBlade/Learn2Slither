import pygame as pg


def get_new_direction(action):
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


def is_valid_move(snake, new_target):
    """Check if the move is valid (not reversing into self)."""
    if len(snake) == 1:
        return
    return new_target == snake[1]


def get_reward(plan, target):
    """Calculate the reward for the current move."""
    if plan[target[0]][target[1]] in ['W', 'S']:
        return -10
    elif plan[target[0]][target[1]] == 'G':
        return 10
    elif plan[target[0]][target[1]] == 'R':
        return -5
    elif plan[target[0]][target[1]] == 0:
        return -0.1
    else:
        return 0
