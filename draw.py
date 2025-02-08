import pygame as pg


def draw_board(screen, plan, direction):
    screen.fill('#EFE1AB')
    background = pg.image.load("textures/l2s-map.png")
    background = scale_background(background, screen.get_width())
    screen.blit(background, (0, 50))

    textures = {
        'R': pg.image.load("textures/tnt.png"),
        'G': pg.image.load("textures/gold.png"),
        'H': {
            (0, 1): pg.image.load("textures/knight-right.png"),
            (0, -1): pg.image.load("textures/knight-left.png"),
            (1, 0): pg.image.load("textures/knight-down.png"),
            (-1, 0): pg.image.load("textures/knight-up.png"),
        },
        'S': pg.image.load("textures/pawn.png"),
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
            if cell == 'H':
                head_texture = scaled_textures[cell][direction]
                screen.blit(head_texture, (x, y))
            elif cell in scaled_textures:
                screen.blit(scaled_textures[cell], (x, y))


def scale_background(image, screen_size):
    return pg.transform.scale(image, (screen_size, screen_size))


def scale_textures(textures, size):
    scaled = {}
    for key, img in textures.items():
        if isinstance(img, dict):
            scaled[key] = {
                dir_key: pg.transform.scale(dir_img, (size, size))
                for dir_key, dir_img in img.items()
            }
        else:
            scaled[key] = pg.transform.scale(img, (size, size))
    return scaled


def draw_score(font, screen, score, best_score):
    """
    Render the score on the screen.
    """
    banner = pg.image.load("textures/banner.png")
    banner = pg.transform.scale(banner, (screen.get_width(), 50))
    screen.blit(banner, (0, 0))
    info = f"Score: {score}    Best: {best_score}"
    score_surface = font.render(info, True, ('#885558'))
    screen.blit(score_surface, (screen.get_width() / 3, 20))
