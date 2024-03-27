import pygame
import math
import sys
import random

pygame.init()

# Screen
WIDTH = 300
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (80, 80))

# Fonts
END_FONT = pygame.font.SysFont('arial', 40)

def draw_grid():
    gap = WIDTH // ROWS
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)

def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)
            game_array[i][j] = (x, y, "", True)

    return game_array

def click(game_array):
    global x_turn, o_turn, images

    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's the player's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)

def system_move(game_array):
    global x_turn, o_turn, images

    best_score = -float('inf')
    best_move = None

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False)
                score = minimax(game_array, 0, False)
                game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], "", True)

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    i, j = best_move
    x, y, char, can_play = game_array[i][j]
    images.append((x, y, O_IMAGE))
    x_turn = True
    o_turn = False
    game_array[i][j] = (x, y, 'o', False)

def minimax(game_array, depth, is_maximizing):
    if has_won(game_array, 'o'):
        return 1
    if has_won(game_array, 'x'):
        return -1
    if has_drawn(game_array):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                if game_array[i][j][2] == "":
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False)
                    score = minimax(game_array, depth + 1, False)
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], "", True)
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                if game_array[i][j][2] == "":
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'x', False)
                    score = minimax(game_array, depth + 1, True)
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], "", True)
                    best_score = min(score, best_score)
        return best_score

def has_won(game_array, player):
    for row in range(len(game_array)):
        if all(game_array[row][col][2] == player for col in range(ROWS)):
            return True

    for col in range(len(game_array)):
        if all(game_array[row][col][2] == player for row in range(ROWS)):
            return True

    if all(game_array[i][i][2] == player for i in range(ROWS)) or all(game_array[i][ROWS - i - 1][2] == player for i in range(ROWS)):
        return True

    return False

def has_drawn(game_array):
    return all(game_array[i][j][2] != "" for i in range(ROWS) for j in range(ROWS))

def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def render():
    win.fill(WHITE)
    draw_grid()

    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()

def reset_game():
    global images, x_turn, o_turn
    images = []
    x_turn = True
    o_turn = False
    return initialize_grid()

def display_options():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if 100 <= m_x <= 200 and 200 <= m_y <= 250:
                    return True
                elif 100 <= m_x <= 200 and 300 <= m_y <= 350:
                    pygame.quit()
                    sys.exit()

        win.fill(WHITE)
        new_match_text = END_FONT.render("New Match", 1, BLACK)
        quit_text = END_FONT.render("Quit", 1, BLACK)
        win.blit(new_match_text, ((WIDTH - new_match_text.get_width()) // 2, 200))
        win.blit(quit_text, ((WIDTH - quit_text.get_width()) // 2, 300))
        pygame.display.update()


def main():
    global x_turn, o_turn, images, draw

    run = True

    while run:
        game_array = reset_game()  # Reset the game state for a new match

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN and x_turn and not has_won(game_array, 'x') and not has_drawn(game_array):
                    click(game_array)

            if not x_turn and not has_won(game_array, 'o') and not has_drawn(game_array):
                system_move(game_array)

            render()

            if has_won(game_array, 'x'):
                display_message("Player 1 has won!")
                break
            elif has_won(game_array, 'o'):
                display_message("Players 2 has won!")
                break
            elif has_drawn(game_array):
                display_message("It's a draw!")
                break

            pygame.display.flip()

        # Display the options for a new match or quitting
        if not display_options():
            run = False

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()


