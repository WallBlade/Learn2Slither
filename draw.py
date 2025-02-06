import pygame as pg
import sys

def draw_board(screen, plan):
    # Draw the 10x10 board
    screen.fill('#CFE1BB')

    # Define the color map
    color_map = {
        0: '#B6C99B',
        'R': 'red',
        'G': 'green',
        'H': 'blue',
        'S': 'black',
        'W': '#88986C',
    }
    rect_size = screen.get_width() // len(plan)
    actual_size = rect_size * len(plan)
    offset = (screen.get_width() - actual_size) // 2

    # Draw the board
    for row_idx, row in enumerate(plan):
        for col_idx, cell in enumerate(row):
            x = offset + col_idx * rect_size
            y = offset + row_idx * rect_size + 50
            color = color_map.get(cell)
            pg.draw.rect(screen, color, (x, y, rect_size, rect_size))

def draw_menu(selected_option, events, agent, screen, font, pause, running, file_path):
    menu_options = ['Resume', 'Save', 'Quit']
    num_options = len(menu_options)

    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                selected_option = (selected_option - 1) % num_options
            elif event.key == pg.K_DOWN:
                selected_option = (selected_option + 1) % num_options
            elif event.key == pg.K_RETURN:
                if selected_option == 0:
                    pause = False
                elif selected_option == 2:
                    agent.save_model(file_path)
                elif selected_option == 3:
                    running = False
                    pg.quit()
                    sys.exit()

    screen.fill('#CFE1BB')

    for i, option in enumerate(menu_options):
        # Highlight the selected option
        if i == selected_option:
            color = '#738357'  # Selected
        else:
            color = '#000000'  # Unselected

        text = font.render(option, True, color)
        screen.blit(text, (100, 50 + i * 50))

    # Update the display
    pg.display.flip()
    
def draw_score(font, screen, score, best_score):
    """
    Render the score on the screen.
    """
    score_surface = font.render(f"Score: {score} Best: {best_score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 15))
