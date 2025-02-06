import pygame as pg
import sys



def draw_board(screen, plan):
    # Draw the 10x10 board
    screen.fill('#CFE1BB')
    background = pg.image.load("textures/background.png")
    background = scale_background(background, screen.get_width())
    screen.blit(background, (0, 50))
    # Define the color map
    textures = {
        0: pg.image.load("textures/grass.png"),
        'R': pg.image.load("textures/grass.png"),
        'G': pg.image.load("textures/grass.png"),
        'H': pg.image.load("textures/grass.png"),
        'S': pg.image.load("textures/grass.png"),
        'W': pg.image.load("textures/grass.png"),
    }
    rect_size = screen.get_width() // len(plan)
    actual_size = rect_size * len(plan)
    offset = (screen.get_width() - actual_size) // 2

    scaled_textures = scale_textures(textures, rect_size)

    # Draw the board
    for row_idx, row in enumerate(plan):
        for col_idx, cell in enumerate(row):
            x = offset + col_idx * rect_size
            y = offset + row_idx * rect_size + 50
            if cell in scaled_textures:
                screen.blit(scaled_textures[cell], (x, y))
            else:
                pg.draw.rect(screen, '#B6C99B', (x, y, rect_size, rect_size))

def scale_background(image, screen_size):
    return pg.transform.scale(image, (screen_size, screen_size))

def scale_textures(textures, size):
    return {key: pg.transform.scale(img, (size, size)) for key, img in textures.items()}
    
def draw_score(font, screen, score, best_score):
    """
    Render the score on the screen.
    """
    score_surface = font.render(f"Score: {score} Best: {best_score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 15))
