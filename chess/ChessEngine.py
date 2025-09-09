"""
This class is responsible for storing all the information about the current state of a game
and also be responsible for determining moves that are valid in the current state & keep a move log
"""



class GameState():
    def __init__(self):
        #8x8 two dimenstional list, each element of the board has 2 characters
        #The first characters denotes the color of the pieces the second character denotes type of piece
        #The string "--" denotes an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.whiteToMove = True
        self.moveLog = []

    #Takes a move as a paremeter and executes it wont work for special moves castling , pawn promotion etx
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move to kee history and undo
        self.whiteToMove = not self.whiteToMove #no longer white turn and thus swap players

    """
    Undo the last move that was made
    """
    def undoMove(self):
        if len(self.moveLog) != 0:#makes sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns

    """
    All moves that consider checks
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves() #not thinking about check rn


    """
    All moves not considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #Number of rows
            for c in range(len(self.board[r])): #Number of columns in a given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) and (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == "p":
                        self.getPawnMoves(r,c, moves)
                    elif piece == "R" :
                        self.getRookMoves(r,c,moves)
        return moves


    """
    Get all the pawn moves located at row and column r & c, add these to the moves list
    """
    def getPawnMoves(self,r,c,moves):
        pass


    """
    Get all rook moves located at row , col  and add these to the move list 
    """
    def getRookMoves(self,r,c,moves):
        pass
class Move():
    #maping keys to values
    #key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow *1000 + self.startCol *100 + self.endRow*10 + self.endCol
        print(self.moveId)

    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False


    def getChessNotation(self):
        #can stuff to make it like the official notation
        return self.pieceMoved+ " "+ self.getRankFile(self.startRow, self.startCol)+"-->" + self.getRankFile(self.endRow, self.endCol )

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
