"""
main file for chess auto player
"""
from __future__ import print_function

import chessPlayer_tree as tree

def initboard():
    """
    initialises a few chess boards
    """
    # normal board ######################
    pawn = 0
    knight = 1
    bishop = 2
    rook = 3
    queen = 4
    king = 5
    side = 10
    board0 = []
    for i in range(0, 64):
        board0.append(0)

    # white
    board0[0] = side + rook
    board0[1] = side + knight
    board0[2] = side + bishop
    board0[3] = side + king
    board0[4] = side + queen
    board0[5] = side + bishop
    board0[6] = side + knight
    board0[7] = side + rook
    for i in range(8, 16):
        board0[i] = side + pawn

    side = 20
    # black
    board0[56] = side + rook
    board0[57] = side + knight
    board0[58] = side + bishop
    board0[59] = side + king
    board0[60] = side + queen
    board0[61] = side + bishop
    board0[62] = side + knight
    board0[63] = side + rook
    for i in range(48, 56):
        board0[i] = side + pawn


    # without pawns #####################
    board1 = []
    for i in range(0, 64):
        board1.append(0)
    side = 10
    # white
    board1[0] = side + rook
    board1[1] = side + knight
    board1[2] = side + bishop
    board1[3] = side + king
    board1[4] = side + queen
    board1[5] = side + bishop
    board1[6] = side + knight
    board1[7] = side + rook

    side = 20
    # black
    board1[56] = side + rook
    board1[57] = side + knight
    board1[58] = side + bishop
    board1[59] = side + king
    board1[60] = side + queen
    board1[61] = side + bishop
    board1[62] = side + knight
    board1[63] = side + rook

    # stalemate scenario ####################
    board2 = []
    for i in range(0, 64):
        board2.append(0)

    # white king
    side = 10
    board2[0] = side + king
    # black queen and king
    side = 20
    board2[10] = side + queen
    board2[63] = side + king

    return [board0, board1, board2]

def GetPlayerPositions(board):
    """
    gets positions occupied, strength
    Note: old version has "player" parameter
    :param board: chess board (list of length 64, offset of 10 for white, offset of 20 for black
    :return: list of occupied spots by white, black (depending on param player), strength of white, black
    """
    whitePos = []
    blackPos = []
    for i in range(len(board)):
        if board[i]/10 == 1:
            whitePos.append(i)
        elif board[i]/10 == 2:
            blackPos.append(i)
    return[whitePos, blackPos]

def EvalBoard(board):
    """
    gives the evaluation of the board (i.e. white values - black values)
    :param board:
    :return: float
    """
    whiteVal = 0
    secondrowWhite = [8, 9, 10, 11, 12, 13, 14, 15]
    blackVal = 0
    secondrowBlack = [48, 49, 50, 51, 52, 53, 54, 55]
    for i in range(len(board)):
        if board[i]/10 == 1:
            # white
            if board[i] == 10:
                # pawn
                whiteVal += 1
                # check for doubled, blocked, isolated pawns
                # if board[i+8] != 0 or (not(i in secondrowWhite) and not(board[i-7] != 10 or board[i-9] != 10)):
                #     whiteVal -= 0.5

                # check for isolated pawns
                if not(i in secondrowWhite) and not(board[i-7] != 10 or board[i-9] != 10):
                    whiteVal -= 0.5
            elif board[i] == 11:
                # knight
                whiteVal += 3
            elif board[i] == 12:
                # bishop
                whiteVal += 3
            elif board[i] == 13:
                # rook
                whiteVal += 5
            elif board[i] == 14:
                # queen
                whiteVal += 9
            elif board[i] == 15:
                # king
                whiteVal += 100000
            else:
                raise ValueError
            # legalmoves = GetPieceLegalMoves(board, i)
            # whiteVal += (0.1*len(legalmoves))
        elif board[i] / 10 == 2:
            # black
            if board[i] == 20:
                # pawn
                blackVal += 1
                # check for doubled, blocked, isolated pawns
                # if board[i-8] != 0 or (not(i in secondrowBlack) and (board[i+7] != 20 or board[i+9] != 20)):
                #     blackVal -= 0.5

                # check for isolated pawns
                if not(i in secondrowBlack) and (board[i+7] != 20 or board[i+9] != 20):
                    blackVal -= 0.5
            elif board[i] == 21:
                # knight
                blackVal += 3
            elif board[i] == 22:
                # bishop
                blackVal += 3
            elif board[i] == 23:
                # rook
                blackVal += 5
            elif board[i] == 24:
                # queen
                blackVal += 9
            elif board[i] == 25:
                # king
                blackVal += 100000
            else:
                raise ValueError
            # legalmoves = GetPieceLegalMoves(board, i)
            # blackVal += (0.1 * len(legalmoves))

    return whiteVal - blackVal

def GetPieceLegalMoves(board,position):
    """

    :param board: chess board
    :param position: pos of piece
    :return: list of legal positions that the piece in <position> can move to
    """

    # checking if the position is occupied
    if board[position] == 0:
        return
    else:
        side = board[position]/10

    # SETUP: ############################################################################

    # the location of the vertical edges of the chessboard
    leftedgepos = [0, 8, 16, 24, 32, 40, 48, 52, 56]
    rightedgepos = [7, 15, 23, 31, 39, 47, 55, 63]

    # location of top and bottom edges
    topendpos = [0, 1, 2, 3, 4, 5, 6, 7]
    botendpos = [56, 57, 58, 59, 60, 61, 62, 63]

    #####################################################################################

    if board[position]%10 == 0:
        legalpos = GetPawnLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 1:
        # knight
        legalpos = GetKniLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 2:
        # bishop
        legalpos = GetBishLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 3:
        # rook
        legalpos = GetRookLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 4:
        # queen
        legalpos = GetQueenLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 5:
        # king
        allmoves = GetKingLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        # print(allmoves)
        legalpos = GetPieceLegalMovesKing(board, position, allmoves)
    else:
        raise ValueError
    # print("getpiecelegalmoves",legalpos)

    return legalpos

def IsPositionUnderThreat(board,position,player):
    """
    returns true if given position is under threat by opponent
    :param board:
    :param position:
    :param player: 10 - white // 20 - black
    :return:
    """
    opponentmoves = []
    if player == 10:
        for pos in range(len(board)):
            if board[pos] >= 20:
                opponentmoves += GetPieceLegalMovesNoKingCheck(board, pos)
    elif player == 20:
        for pos in range(len(board)):
            if board[pos] >= 10 and board[pos] < 20:
                opponentmoves += GetPieceLegalMovesNoKingCheck(board, pos)
    else:
        raise ValueError

    if position in opponentmoves:
        return True
    else:
        return False

# ~~~~~~~~~~~~~~Main Algorithm~~~~~~~~~~~~~~~~~ #

def Minimize(board, recursion_depth, player, alpha, beta):
    """

    :param player: 10 white 20 black
    :param board:
    :param recursion_depth:
    :param alpha: upper bound
    :param beta: lower bound
    :return: (board, evaluation, alpha, beta, moves tree) (list, float, int, int, tree list)
    """
    positions = GetPlayerPositions(board)

    # base case
    if recursion_depth == 0:
        return [board, 0-EvalBoard(board), -1000000, 1000000, []]

    # recursive step
    else:
        # determine current positions
        if player == 10:
            selfPos = positions[0]
            opp = 20
        elif player == 20:
            selfPos = positions[1]
            opp = 10
        else:
            raise ValueError
        # setup
        minStrengthDiff = 1000000
        newboard = []
        endTree = False
        treelist = []
        # begin algorithm
        for pos in selfPos:
            piecelegalmoves = GetPieceLegalMoves(board, pos)
            for newpos in piecelegalmoves:
                oldpiece = MakeMove(board, pos, newpos)
                if InCheck(board, player):
                    UnMakeMove(board, newpos, pos, oldpiece)
                    break
                movestree = tree.tree([[pos, newpos]])
                treelist.append(movestree)
                values = Maximize(board, recursion_depth-1, opp, alpha, beta) # returns: (board, evaluation, alpha, beta, moves tree)
                strengthDiff = values[1] # eval value
                movestree.store[0].append(strengthDiff)
                alpha = values[2]
                beta = values[3]
                if recursion_depth > 1:
                    # movestree.store[1].append(values[4])
                    movestree.store[1] += values[4]
                if strengthDiff < alpha:
                    # white would not let that happen
                    minStrengthDiff = strengthDiff
                    UnMakeMove(board, newpos, pos, oldpiece)
                    endTree = True
                    break
                if strengthDiff < minStrengthDiff:
                    # found a better (lower) value
                    minStrengthDiff = strengthDiff
                    beta = minStrengthDiff
                    newboard = board[:]
                UnMakeMove(board, newpos, pos, oldpiece)
            if endTree:
                break
        return [newboard, minStrengthDiff, alpha, beta, treelist]

def Maximize(board, recursion_depth, player, alpha, beta):
    """

    :param board:
    :param recursion_depth:
    :param player: 10 white 20 black
    :param alpha: upper bound
    :param beta: lower bound
    :param movestree: the tree
    :return: (board, evaluation, alpha, beta, moves tree) (list, float, int, int, treelist)
    """
    positions = GetPlayerPositions(board)
    # base case
    if recursion_depth == 0:
        return [board, EvalBoard(board), -1000000, 1000000, []]

    # recursive step
    else:
        # determine current positions
        if player == 10:
            selfPos = positions[0]
            opp = 20
        elif player == 20:
            selfPos = positions[1]
            opp = 10
        else:
            raise ValueError
        # setup
        maxStrengthDiff = -1000000
        newboard = []
        endTree = False
        treelist = []
        # begin algorithm
        for pos in selfPos:
            piecelegalmoves = GetPieceLegalMoves(board, pos)
            for newpos in piecelegalmoves:
                oldpiece = MakeMove(board, pos, newpos)
                if InCheck(board, player):
                    UnMakeMove(board, newpos, pos, oldpiece)
                    break
                movestree = tree.tree([[pos, newpos]])
                treelist.append(movestree)
                values = Minimize(board, recursion_depth-1, opp, alpha, beta) # returns (board, evaluation, alpha, beta, moves tree)
                strengthDiff = values[1]
                movestree.store[0].append(strengthDiff)
                alpha = values[2]
                beta = values[3]
                if recursion_depth > 1:
                    # movestree.store[1].append(values[4])
                    movestree.store[1] += values[4]
                if strengthDiff > beta:
                    # black will not let that happen
                    maxStrengthDiff = strengthDiff
                    UnMakeMove(board, newpos, pos, oldpiece)
                    endTree = True
                    break
                if strengthDiff > maxStrengthDiff:
                    # found best value for white (alpha)
                    maxStrengthDiff = strengthDiff
                    alpha = maxStrengthDiff
                    newboard = board[:]
                UnMakeMove(board, newpos, pos, oldpiece)
            if endTree:
                break
        return [newboard, maxStrengthDiff, alpha, beta, treelist]

def GenWhiteCandidateMove(board):
    """
    Generates candidate move for white. Need to modify before final submission
    for now, just update the board accordingly
    :param board:
    :return:
    """
    values = Maximize(board, 3, 10, -1000000, 1000000)
    newtree = tree.tree([[0,0],0])
    newtree.store[1] = values[4]
    return [values[0], values[1], values[2], values[3], newtree]

def GenBlackCandidateMove(board):
    """
    Generates candidate move for black. Need to modify before final submission
    for now, just update the board accordingly
    :param board:
    :return:
    """
    values = Minimize(board, 3, 20, -1000000, 1000000)
    newtree = tree.tree([[0,0],0])
    newtree.store[1] = values[4]
    return [values[0], values[1], values[2], values[3], newtree]

def chessPlayer(board, player):
    """

    :param board:
    :param player:
    :return: [ status, move, candidateMoves, evalTree]
    note the following:
    status = bool
    move = [initial, final] = [int, int]
    candidateMoves = [[int,int], [int,int],...]

    """
    status = True
    move = []
    candidateMoves = []
    lvltraversal = []
    if player != 10 and player != 20 or len(board)!=64:
        status = False
        return [status, move, candidateMoves, lvltraversal]

    if player == 10:
        values = GenWhiteCandidateMove(board)
        lvltraversal = values[4].Get_LevelOrder()
        higheststrength = -1000000
        for tree in values[4].store[1]:
            candidateMoves.append([tree.store[0][0], tree.store[0][1]])
            if tree.store[0][1] > higheststrength:
                higheststrength = tree.store[0][1]
                move = [tree.store[0][0], tree.store[0][1]]
    else:
        values = GenBlackCandidateMove(board)
        lvltraversal = values[4].Get_LevelOrder()
        higheststrength = 1000000
        for tree in values[4].store[1]:
            candidateMoves.append([[tree.store[0][0], tree.store[0][1]], tree.store[1]])
            if tree.store[0][1] < higheststrength:
                higheststrength = tree.store[0][1]
                move = [tree.store[0][0], tree.store[0][1]]

    return [status, move, candidateMoves, lvltraversal]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Helper Functions ###################################################################################################

# printing the board #

def printboard(board):
    """
    prints the current board
    :param board: chess board in list format
    :return: None
    """
    print ("\n")
    for i in range(len(board)-1, -1, -1):

        if board[i] >= 20:
            if board[i]%20 == 0:
                print (" BP ", end="")
            elif board[i]%20 == 1:
                print (" BN ", end="")
            elif board[i]%20 == 2:
                print (" BB ", end="")
            elif board[i]%20 == 3:
                print (" BR ", end="")
            elif board[i]%20 == 4:
                print (" BQ ", end="")
            elif board[i]%20 == 5:
                print (" BK ", end="")
            else:
                raise ValueError
        elif board[i] >= 10 and board[i] < 20:
            if board[i]%10 == 0:
                print(" WP ", end="")
            elif board[i]%10 == 1:
                print (" WN ", end="")
            elif board[i]%10 == 2:
                print (" WB ", end="")
            elif board[i]%10 == 3:
                print (" WR ", end="")
            elif board[i]%10 == 4:
                print (" WQ ", end="")
            elif board[i]%10 == 5:
                print (" WK ", end="")
            else:
                raise ValueError
        elif board[i] == 0:
            print (" -- ", end="")
        else:
            raise ValueError
        if i>7 and i%8 == 0:
            print ("\n")

# helper functions for GetPieceLegalMoves #

def GetPieceLegalMovesNoKingCheck(board,position):
    """
    All "moves" that the piece threatens -> use ONLY in IsPositionUnderThreat and GetPieceLegalMovesKing
    :param board: chess board
    :param position: pos of piece
    :return: list of legal positions that the piece in <position> can move to
    """
    # print(board)
    # checking if the position is occupied
    if board[position] == 0:
        return
    else:
        side = board[position]/10

    # SETUP: ############################################################################

    # the location of the vertical edges of the chessboard
    leftedgepos = [0, 8, 16, 24, 32, 40, 48, 52, 56]
    rightedgepos = [7, 15, 23, 31, 39, 47, 55, 63]

    # location of top and bottom edges
    topendpos = [0, 1, 2, 3, 4, 5, 6, 7]
    botendpos = [56, 57, 58, 59, 60, 61, 62, 63]

    legalpos = []
    # current row of the piece (0 <= row <= 7)
    # row = position/8

    #####################################################################################

    if board[position]%10 == 0:
        legalpos += GetPawnLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 1:
        # knight
        legalpos += GetKniLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 2:
        # bishop
        legalpos += GetBishLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 3:
        # rook
        legalpos += GetRookLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 4:
        # queen
        legalpos += GetQueenLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)

    elif board[position]%10 == 5:
        # king
        # all squares that king can threaten
        legalpos += GetKingLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    else:
        raise ValueError
    # print("getpiecelegalmovesnokingcheck",legalpos)

    return legalpos

def GetPieceLegalMovesKing(board, position, allmoves):
    """
    Precondition: position must be a king
    :param board:
    :param position: position of the king on the board
    :param allmoves: including ones that will put king in check
    :return: list of legal moves
    """
    if board[position]/10 == 1:
        side = 10
        opponentK = 25
    elif board[position]/10 == 2:
        side = 20
        opponentK = 15
    else:
        raise ValueError

    opponentKlegalmoves = []
    # Opponent king
    for index in range(len(board)):
        if board[index] == opponentK:
            opponentKlegalmoves += GetPieceLegalMovesNoKingCheck(board, index)
            break
    toberemoved = []
    for pos in allmoves:
        if IsPositionUnderThreat(board, pos, side) or pos in opponentKlegalmoves:
            toberemoved.append(pos)

    if toberemoved != []:
        for pos in toberemoved:
            allmoves.remove(pos)

    return allmoves

# helper functions for algorithm #

def InCheck(board,player):
    """
    find the king and see if it is in check
    :param board: chess board
    :return: boolean
    """
    for i in range(len(board)):
        if board[i] == 15 and player == 10:
            if IsPositionUnderThreat(board, i, 10):
                return True
        elif board[i] == 25 and player == 20:
            if IsPositionUnderThreat(board, i, 20):
                return True
    return False

def MakeMove(board, position, newposition):
    """
    Precondition: new position is in legal moves
    moves piece into new position
    :param board:
    :param position:
    :param newposition:
    :return: taken piece (0 if piece not taken)
    """
    # old code
    # if newposition not in GetPieceLegalMoves(board, position):
    #     print ("illegal move")
    #     raise ValueError
    # elif board[position] == 0:
    #     print ("nothing to move")
    #     raise ValueError

    # newboard = board[:]
    # piece = board[position]
    # newboard[newposition] = piece
    # newboard[position] = 0
    # return newboard

    # new code (eliminates O(n) list traversal of GetLegalMoves)
    if board[position] == 0:
        print("nothing to move")
        raise ValueError

    # new code (eliminates O(n) copying)
    oldpiece = board[newposition]
    currpiece = board[position]
    board[position] = 0
    board[newposition] = currpiece
    return oldpiece

def UnMakeMove(board, position, oldposition, oldpiece):
    """
    Precondition: old position has nothing in it and is legit in terms of moves
    unmakes a move (modifies board to become original board)
    :param board: chess board
    :param position: "new position"
    :param oldposition: old position
    :param oldpiece: old piece (0 if no old i.e. "taken" piece)
    :return: None (void)
    """
    piece = board[position]
    board[oldposition] = piece
    board[position] = oldpiece

# Helper functions for GetPieceLegalMoves #

def GetPawnLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    returns a list of legal positions for a pawn
    :param board: chess board (list of length 64)
    :param position: current position
    :param side: black/white
    :param leftedgepos: left constraints
    :param rightedgepos: right constraints
    :param topendpos: top row constraints
    :param botendpos: bot row constraints
    :return: list of legal positions
    """
    legalpos = []
    if side == 1:
        # white pawn
        # check if it can go forward (includes violating board position constraints)
        if position + 8 < 64:
            if board[position + 8] == 0:
                legalpos.append(position+8)
        # now check if it can capture diagonally
        if position in leftedgepos:
            # check if it can capture diagonally right
            if position+8+1 < 64 and not (position in botendpos):
                if board[position + 8 + 1] / 10 == 2:
                    # if it is the opponent (black) piece, can capture
                    legalpos.append(position + 8 + 1)
        elif position in rightedgepos:
            # check if it can capture diagonally left
            if position+8-1 < 64 and not (position in botendpos):
                if board[position + 8 - 1] / 10 == 2:
                    # if it is the opponent (black) piece, can capture
                    legalpos.append(position + 8 - 1)
        else:
            # not on the edge, can capture both ways
            # check if it can capture diagonally right
            if position + 8 + 1 < 64 and not (position in botendpos):
                if board[position+8+1] / 10 == 2:
                    # if it is the opponent (black) piece, can capture
                    legalpos.append(position + 8 + 1)
            # check if it can capture diagonally left
            if position + 8 - 1 < 64 and not (position in botendpos):
                if board[position + 8 - 1] / 10 == 2:
                    # if it is the opponent (black) piece, can capture
                    legalpos.append(position + 8 - 1)
        return legalpos
    elif side == 2:
        # black pawn
        # check if it can go forward
        if position - 8 >= 0:
            if board[position - 8] == 0:
                legalpos.append(position-8)
        # now check if it can capture diagonally
        if position in leftedgepos:
            # check if it can capture diagonally right
            if position - 8 + 1 >= 0 and not (position in topendpos):
                if board[position - 8 + 1] / 10 == 1:
                    # if it is the opponent (w) piece, can capture
                    legalpos.append(position - 8 + 1)
        elif position in rightedgepos:
            # check if it can capture diagonally left
            if position - 8 - 1 >= 0 and not (position in topendpos):
                if board[position - 8 - 1] / 10 == 1:
                    # if it is the opponent (w) piece, can capture
                    legalpos.append(position - 8 - 1)
        else:
            # not on the edge, can capture both ways
            # check if it can capture diagonally right
            if position - 8 + 1 >= 0 and not (position in topendpos):
                if board[position - 8 + 1] / 10 == 1:
                    # if it is the opponent (w) piece, can capture
                    legalpos.append(position - 8 + 1)
            # check if it can capture diagonally left
            if position - 8 - 1 >= 0 and not (position in topendpos):
                if board[position - 8 - 1] / 10 == 1:
                    # if it is the opponent (w) piece, can capture
                    legalpos.append(position - 8 - 1)
    return legalpos

def GetKniLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """

    :param board: chess board
    :param position: current position of knight
    :param side: black or white (2 or 1)
    :param leftedgepos: left edge positions
    :param rightedgepos: right edge positions
    :param topendpos: top row constraints
    :param botendpos bottom row constraints
    :return: list of legal positions for knight
    """
    legalpos = []

    innerleftedge = [17, 25, 33, 41]
    innerrightedge = [22, 30, 38, 46]
    innertopedge = [10, 11, 12, 13]
    innerbotedge = [50, 51, 52, 53]

    # define possible positions without checking
    # first letter: D - down; U - up; L - left; R - right
    # move three squares in the dir of the first letter then one square in the dir of the second letter

    kniUL = position - 2*8 - 1
    kniLU = position - 2 - 8
    kniLD = position - 2 + 8
    kniDL = position + 2*8 - 1
    kniDR = position + 2*8 + 1
    kniRD = position + 2 + 8
    kniRU = position + 2 - 8
    kniUR = position - 2*8 + 1

    # cover all possible cases
    if position in topendpos and position in leftedgepos:
        # upper left corner
        legalpos.append(kniRD)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in topendpos and position in rightedgepos:
        # upper right corder
        legalpos.append(kniLD)
        legalpos.append(kniDL)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in botendpos and position in leftedgepos:
        # lower left corner
        legalpos.append(kniUR)
        legalpos.append(kniRU)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in botendpos and position in rightedgepos:
        # lower right corner
        legalpos.append(kniUL)
        legalpos.append(kniLU)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 1:
        legalpos.append(kniRD)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 8:
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 6:
        legalpos.append(kniLD)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 15:
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        legalpos.append(kniDL)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 48:
        legalpos.append(kniRD)
        legalpos.append(kniRU)
        legalpos.append(kniUL)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 57:
        legalpos.append(kniUR)
        legalpos.append(kniUL)
        legalpos.append(kniLU)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 55:
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        legalpos.append(kniUL)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 62:
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        legalpos.append(kniLU)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 9:
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 14:
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 49:
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position == 54:
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in innerleftedge:
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in innerrightedge:
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in innertopedge:
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in innerbotedge:
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in topendpos:
        legalpos.append(kniLD)
        legalpos.append(kniRD)
        legalpos.append(kniDR)
        legalpos.append(kniDL)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in botendpos:
        legalpos.append(kniLU)
        legalpos.append(kniRU)
        legalpos.append(kniUL)
        legalpos.append(kniUR)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in rightedgepos:
        legalpos.append(kniUL)
        legalpos.append(kniDL)
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    elif position in leftedgepos:
        legalpos.append(kniUR)
        legalpos.append(kniDR)
        legalpos.append(kniRU)
        legalpos.append(kniRD)
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos
    else:
        legalpos.append(kniUL)
        legalpos.append(kniLU)
        legalpos.append(kniLD)
        legalpos.append(kniDL)
        legalpos.append(kniDR)
        legalpos.append(kniRD)
        legalpos.append(kniRU)
        legalpos.append(kniUR)
        # delete from possible spots all the spots occupied by one's own pieces
        toberemoved = []
        for p in legalpos:
            if board[p] != 0:
                if board[p] / 10 == side:
                    toberemoved.append(p)
        for pos in toberemoved:
            legalpos.remove(pos)
        return legalpos

def GetBishLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """

    :param board: chess board
    :param position: current position of bishop
    :param side: black or white (2 or 1)
    :param leftedgepos: left edge positions
    :param rightedgepos: right edge positions
    :param topendpos: top row constraints
    :param botendpos bottom row constraints
    :return: list of legal positions for bishop
    """
    legalpos = []
    if position in leftedgepos:
        # go diagonally EAST
        legalpos += northeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += southeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    elif position in rightedgepos:
        # go diagonally WEST
        legalpos += northwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += southwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    elif position in topendpos:
        legalpos += southwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += southeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    elif position in botendpos:
        legalpos += northwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += northeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    else:
        # go diagonally anywhere
        legalpos += northeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += southeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += northwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
        legalpos += southwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    return legalpos

def GetRookLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """

    :param board: chess board
    :param position: current position of bishop
    :param side: black or white (2 or 1)
    :param leftedgepos: left edge positions
    :param rightedgepos: right edge positions
    :param topendpos: top row constraints
    :param botendpos bottom row constraints
    :return: list of legal positions for bishop
    """
    legalpos = []
    legalpos += west(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += east(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += north(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += south(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    return legalpos

def GetQueenLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """

    :param board: chess board
    :param position: current position of bishop
    :param side: black or white (2 or 1)
    :param leftedgepos: left edge positions
    :param rightedgepos: right edge positions
    :param topendpos: top row constraints
    :param botendpos bottom row constraints
    :return: list of legal positions for queen
    """
    # TODO: check edge cases
    legalpos = []
    legalpos += northwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += northeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += southwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += southeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += west(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += east(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += north(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    legalpos += south(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos)
    return legalpos

def GetKingLegalMoves(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """

    :param board: chess board
    :param position: current position of bishop
    :param side: black or white (2 or 1)
    :param leftedgepos: left edge positions
    :param rightedgepos: right edge positions
    :param topendpos: top row constraints
    :param botendpos bottom row constraints
    :return: list of legal positions for bishop
    """
    legalpos = []

    # define possible positions without checking
    kingN = position - 8
    kingNE = position - 8 + 1
    kingE = position + 1
    kingSE = position + 8 + 1
    kingS = position + 8
    kingSW = position + 8 - 1
    kingW = position - 1
    kingNW = position - 8 - 1

    # cover all possible cases
    if (position in topendpos) and (position in leftedgepos):
        legalpos.append(kingS)
        legalpos.append(kingSE)
        legalpos.append(kingE)
    elif (position in topendpos) and (position in rightedgepos):
        legalpos.append(kingW)
        legalpos.append(kingSW)
        legalpos.append(kingS)
    elif (position in botendpos) and (position in leftedgepos):
        legalpos.append(kingE)
        legalpos.append(kingNE)
        legalpos.append(kingN)
    elif (position in botendpos) and (position in rightedgepos):
        legalpos.append(kingN)
        legalpos.append(kingNW)
        legalpos.append(kingW)
    elif position in topendpos:
        legalpos.append(kingE)
        legalpos.append(kingSE)
        legalpos.append(kingS)
        legalpos.append(kingSW)
        legalpos.append(kingW)
    elif position in botendpos:
        legalpos.append(kingE)
        legalpos.append(kingNE)
        legalpos.append(kingN)
        legalpos.append(kingNW)
        legalpos.append(kingW)
    elif position in rightedgepos:
        legalpos.append(kingN)
        legalpos.append(kingNW)
        legalpos.append(kingW)
        legalpos.append(kingSW)
        legalpos.append(kingS)
    elif position in leftedgepos:
        legalpos.append(kingN)
        legalpos.append(kingNE)
        legalpos.append(kingE)
        legalpos.append(kingSE)
        legalpos.append(kingS)
    else:
        legalpos.append(kingN)
        legalpos.append(kingNE)
        legalpos.append(kingE)
        legalpos.append(kingSE)
        legalpos.append(kingS)
        legalpos.append(kingSW)
        legalpos.append(kingW)
        legalpos.append(kingNW)

    # delete from possible spots all the spots occupied by one's own pieces
    toberemoved = []
    for p in legalpos:
        if board[p] != 0:
            if board[p] / 10 == side:
                toberemoved.append(p)
    for pos in toberemoved:
        legalpos.remove(pos)
    return legalpos

def northwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes northwest until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    northw = position - 8 - 1
    if northw <= 0:
        return legalpos
    while not (northw in topendpos or northw in leftedgepos) and board[northw] == 0:
        legalpos.append(northw)
        northw = northw - 8 - 1

    if (northw in topendpos or northw in leftedgepos) and board[northw] == 0:
        legalpos.append(northw)
        return legalpos
    elif board[northw] != 0:
        if board[northw]/10 == 2 and side == 1:
            legalpos.append(northw)
        elif board[northw]/10 == 1 and side == 2:
            legalpos.append(northw)
        return legalpos
    return legalpos

def northeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes NE until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    northe = position - 8 + 1
    if northe <= 0:
        return legalpos
    while not (northe in topendpos or northe in rightedgepos) and board[northe] == 0:
        legalpos.append(northe)
        northe = northe - 8 + 1

    if (northe in topendpos or northe in rightedgepos) and board[northe] == 0:
        legalpos.append(northe)
        return legalpos
    elif board[northe] != 0:
        if board[northe]/10 == 2 and side == 1:
            legalpos.append(northe)
        elif board[northe]/10 == 1 and side == 2:
            legalpos.append(northe)
        return legalpos
    return legalpos

def southwest(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes SW until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    southw = position + 8 - 1
    if southw >= 63:
        return legalpos
    while not (southw in botendpos or southw in leftedgepos) and board[southw] == 0:
        legalpos.append(southw)
        southw = southw + 8 - 1

    if (southw in botendpos or southw in leftedgepos) and board[southw] == 0:
        legalpos.append(southw)
        return legalpos
    elif board[southw] != 0:
        if board[southw]/10 == 2 and side == 1:
            legalpos.append(southw)
        elif board[southw]/10 == 1 and side == 2:
            legalpos.append(southw)
        return legalpos
    return legalpos

def southeast(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes SE until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    southe = position + 8 + 1
    if southe >= 63:
        return legalpos
    while (not (southe in botendpos or southe in rightedgepos)) and (board[southe] == 0):
        legalpos.append(southe)
        southe = southe + 8 + 1

    if (southe in botendpos or southe in rightedgepos) and board[southe] == 0:
        legalpos.append(southe)
        return legalpos
    elif board[southe] != 0:
        if board[southe]/10 == 2 and side == 1:
            legalpos.append(southe)
        elif board[southe]/10 == 1 and side == 2:
            legalpos.append(southe)
        return legalpos
    return legalpos

def west(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes west until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    curr_row = position/8
    leftbound = curr_row * 8
    w = position - 1
    while w >= leftbound and board[w] == 0:
        legalpos.append(w)
        w -= 1

    if w < leftbound:
        # cleared the row
        return legalpos
    else:
        if board[w]/10 == 2 and side == 1:
            legalpos.append(w)
        elif board[w]/10 == 1 and side == 2:
            legalpos.append(w)
        return legalpos

def east(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes east until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    curr_row = position / 8
    rightbound = curr_row * 8 + 7
    e = position + 1
    while e <= rightbound and board[e] == 0:
        legalpos.append(e)
        e += 1

    if e > rightbound:
        return legalpos
    else:
        if board[e]/10 == 2 and side == 1:
            legalpos.append(e)
        elif board[e]/10 == 1 and side == 2:
            legalpos.append(e)
        return legalpos

def north(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes north until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    curr_row = position / 8
    upbound = position - curr_row * 8
    n = position - 8
    while n >= upbound and board[n] == 0:
        legalpos.append(n)
        n -= 8

    if n < upbound:
        # cleared the column
        return legalpos
    else:
        if board[n]/10 == 2 and side == 1:
            legalpos.append(n)
        elif board[n]/10 == 1 and side == 2:
            legalpos.append(n)
        return legalpos

def south(board, position, side, leftedgepos, rightedgepos, topendpos, botendpos):
    """
    goes south until hits a constraint
    :param board: chess board
    :param position: current position
    :param side: black/white (2 or 1)
    :param leftedgepos: left edge constraints
    :param rightedgepos: right edge constraints
    :param topendpos: top end constraints
    :param botendpos: bottom end constraints
    :return: list of legal positions
    """
    legalpos = []
    curr_row = position / 8
    lowbound = position + (7 - curr_row) * 8
    s = position + 8
    while s <= lowbound and board[s] == 0:
        legalpos.append(s)
        s += 8


    if s > lowbound:
        # cleared the column
        return legalpos
    else:
        if board[s]/10 == 2 and side == 1:
            legalpos.append(s)
        elif board[s]/10 == 1 and side == 2:
            legalpos.append(s)
        return legalpos

# End of Helper Functions ############################################################################################
