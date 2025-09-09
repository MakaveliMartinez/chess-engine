"""
This is the main driver file for the program responsible for user input and displaying the current GameState object
"""

import pygame as p
from pygame import MOUSEBUTTONDOWN
from pygame.examples.moveit import WIDTH

from chess import ChessEngine

WIDTH = HEIGHT = 512 #could also do 400, if bigger get higher res images

DIMENSION = 8 #dimensions of the chess board are 8x8

SQ_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15 #for animation later on

IMAGES = {}

"""
Load images one at a time since it is a fairly expensive operation,
initialize a global dictionary of images
"""

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
        #WE can access any image by saying IMAGES['wp']

"""
Main Driver for our code this will handle all input, and updating graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    loadImages() #Only do this before the while looop
    print(gs.board)
    running = True
    sqSelected = () #initially no square is picked, keep track of users last click (tuple: (row,col))
    playerClicks = [] #Keep track of player clicks (two tuples: [(6,4),(4,4) ] )
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#This is the (x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col): #user clicked the square twice
                    sqSelected = () #deselecting a piece
                    playerClicks = [] #Clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #Appen for both the first and second click
                if len(playerClicks) == 2: #After the second click
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = []

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsible for all the graphics within a current game state
"""
def drawGameState(screen,gs):
    drawBoard(screen) #draw the board
    #add in piece highlighting or move suggestions l8r
    drawPieces(screen,gs.board) #Draw pieces ontop of those squares

"""
Draw the squares on the board
"""
def drawBoard(screen):
    colors = [p.Color("white"),p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color,p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



"""
Draw the pieces using the board using the current game state board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #means if its not an empty square we want to draw our piece here
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE,SQ_SIZE))


if __name__  == "__main__" :
    main()


