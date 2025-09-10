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
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                              'B':self.getBishopMoves,"Q":self.getQueenMoves,'K':self.getKingMoves }

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
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)# Calls appropriate move function based on piece type
        return moves


    """
    Get all the pawn moves located at row and column r & c, add these to the moves list
    """
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #White pawn to move
            if self.board[r-1][c] == "--": # If the square in front is blank move up one
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c] == "--": # this is a two square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c - 1 >= 0: #Respect the bounds of the board capture to the left
                if self.board[r-1][c-1][0] == 'b': #There is an enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
            if c + 1  <= 7: #Capture to the right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c ), (r - 1, c +1), self.board))
        else:
            if self.board[r-5][c] =="--": #Square infront of black pawn go down one
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": #Double pawn move up the board black side
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0: #respect the bounds of board from blacks view
                if self.board[r+1][c-1][0] =='w':
                    moves.append(Move((r, c), (r + 1, c -1), self.board))
            if c + 1 <= 7 :
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c+1), self.board))






    """
    Get all rook moves located at row , col  and add these to the move list 
    """
    def getRookMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Meaning that this is a valid empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # Meaning this is a valid piece we can move to
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break  # stop after capturing
                    else:
                        break
                else:
                    break


    """
    Get all Knight moves located at row, col , add and them to the move list
    """

    def getKnightMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = ((-2,1),(-2,-1),(-1,2),(-1,-2),(2,1),(2,-1),(1,2),(1,-2)) # All the possible moves / direction a Knight can move

        for d in directions:
            #Notice here we got rid of the nested for i in range, this is because the knight has fixed squares it can
            #jump too we needn't calculate all possible moves for it across the entire board, just the current possible
            #moves
            endRow = r + d[0]
            endCol = c + d[1]
            if 0<= endRow< 8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    break
                else:
                    break
            else:
                break


    """
    Get all Bishop moves loacted at row, col and add these to the move list
    """
    def getBishopMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w' # meaning if its white move than the enemy color is b otherwise the enemy color would be w since it would be blacks turn
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) # all possible diagonal squares from the bishop

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0<= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break



    """
    Get all Queen moves located at row, col and add these to the move list
    """
    def getQueenMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = ((-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(0,-1),(1,0),(0,1))

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0<= endRow <8 and 0<= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break



    """
    Get all King moves located at row, col and add these to the move list
    """
    def getKingMoves(self,r,c,moves):
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
        #print(self.moveId)

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
