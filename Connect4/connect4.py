import numpy as np
import pygame
import sys
import math
BLUE = (0,0,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def tablero():
    tabla = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return tabla


def drop_piece(tabla, fila, col, pieza):
    tabla[fila][col] = pieza


def is_valid_location(tabla, col):
    return tabla[ROW_COUNT-1][col] == 0


def get_next_open_row(tabla, col):
    for r in range(ROW_COUNT):
        if tabla[r][col] == 0:
            return r


def print_board(tabla):
    print(np.flip(tabla, 0))

def winning_move(tabla, pieza):
    # Revisar jugadas horizontales ganadoras
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if tabla[r][c] == pieza and tabla[r][c+1] == pieza and tabla[r][c+2] == pieza and tabla[r][c+3] == pieza:
                return True

    # Revisar jugadas verticales ganadoras
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if tabla[r][c] == pieza and tabla[r+1][c] == pieza and tabla[r+2][c] == pieza and tabla[r+3][c] == pieza:
                return True

    # Revisar posibles jugadas diagonales ganadoras
    # Pendiente positiva

    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if tabla[r][c] == pieza and tabla[r+1][c+1] == pieza and tabla[r+2][c+2] == pieza and tabla[r+3][c+3] == pieza:
                return True

    # Pendiente negativa
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if tabla[r][c] == pieza and tabla[r-1][c+1] == pieza and tabla[r-2][c+2] == pieza and tabla[r-3][c+3] == pieza:
                return True

def draw_board(tabla):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if tabla[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

            elif tabla[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                   (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                   RADIUS)

    pygame.display.update()


tabla = tablero()
print_board(tabla)
game_over = False
turno = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2-5)

screen = pygame.display.set_mode(size)

draw_board(tabla)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 30)
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turno == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # Pedir jugada de Jugador 1
            if turno == 0:
                posx= event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(tabla, col):
                    fila = get_next_open_row(tabla, col)
                    drop_piece(tabla, fila, col, 1)

                    if winning_move(tabla, 1):
                        label = myfont.render("¡¡Gano el Jugador 1!! ¡¡Felicidades!!", 1, RED)
                        screen.blit(label, (10,10))
                        game_over =True

            # Pedir jugada del Jugador 2
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(tabla, col):
                        fila = get_next_open_row(tabla, col)
                        drop_piece(tabla, fila, col, 2)

                        if winning_move(tabla, 2):
                            label = myfont.render("¡¡Gano el Jugador 2!! ¡¡Felicidades!!", 1, YELLOW)
                            screen.blit(label, (10, 10))
                            game_over =True

        print_board(tabla)
        draw_board(tabla)

        turno += 1
        turno = turno % 2

        if game_over:
            pygame.time.wait(3000)
