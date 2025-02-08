def get_state(plan, snake, print=False):
    """
    Get the state of the snake from its head in each direction
    """
    y, x = snake[0]

    col_cells = get_col(plan, x, y)
    row_cells = get_row(plan, x, y)

    dangers = check_danger(row_cells, col_cells)
    foods = check_food(row_cells, col_cells)
    if print:
        print_state(col_cells, plan[y], len(row_cells['west']))

    return (*dangers, *foods)


def get_row(plan, x, y):
    row = plan[y]

    return {
        'west': row[:x],
        'east': row[x+1:]
    }


def get_col(plan, x, y):
    return {
        'north': [plan[i][x] for i in range(y)],
        'south': [plan[i][x] for i in range(y+1, len(plan))]
    }


def check_danger(row, col):
    """
    Check for danger on adjacent cells

    Encoding:
    - 0: No danger
    - 1: Wall or Body collision
    """
    dangers = {
        'north': 0,
        'south': 0,
        'east': 0,
        'west': 0,
    }

    if col['north'] and col['north'][-1] in ['W', 'S']:
        dangers['north'] = 1

    if col['south'] and col['south'][0] in ['W', 'S']:
        dangers['south'] = 1

    if row['east'] and row['east'][0] in ['W', 'S']:
        dangers['east'] = 1

    if row['west'] and row['west'][-1] in ['W', 'S']:
        dangers['west'] = 1

    return (dangers['north'], dangers['south'], dangers['east'], dangers['west'])

def find_closest_food(cells):
    for cell in cells:
        if cell == 'G':
            return 1
        if cell == 'R':
            return -1
    return 0


def check_food(row, col):
    """
    Check for closest food in each direction

    Encoding:
    - 0: No food
    - 1: Green Apple
    - -1: Red Apple
    """
    foods = {
        'north': find_closest_food(col['north'][::-1]),
        'south': find_closest_food(col['south']),
        'east': find_closest_food(row['east']),
        'west': find_closest_food(row['west'][::-1]),
    }

    return (foods['north'], foods['south'], foods['east'], foods['west'])


def print_state(col_cells, row, distance):
    def print_column(cells, indent):
        for cell in cells:
            print(' ' * indent + str(cell))

    print_column(col_cells['north'], distance)
    print(''.join(str(x) for x in row))
    print_column(col_cells['south'], distance)
    print()
