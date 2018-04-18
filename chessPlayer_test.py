import timeit
from chessPlayer import *

start_time = timeit.default_timer()
"""
def twoplayer():
    board = initboard()
    finished = False
    while not finished:
        printboard(board)
        whitemove = input("\n White move (position, new position):")
        while (whitemove[1] not in GetPieceLegalMoves(board, whitemove[0])):
            whitemove = input("\n Error, invalid move. White move (position, new position):")
        board = MakeMove(board, whitemove[0], whitemove[1])

        blackmove = input("\n Black move (position, new position):")
        while (blackmove[1] not in GetPieceLegalMoves(board, blackmove[0])):
            blackmove = input("\n Error, invalid move. Black move (position, new position):")
        board = MakeMove(board, blackmove[0], blackmove[1])

        printboard(board)
        finished = input("\n Done?")
"""

#TODO test AI (for both sides)
# def oneplayer():
#     board = initboard()[1][:]
#     finished = False
#     while not finished:
#         printboard(board)
#         print GetPieceLegalMoves(board, 4)
#         whitemove = input("\n White move (position, new position):")
#         while (whitemove[1] not in GetPieceLegalMoves(board, whitemove[0])):
#             whitemove = input("\n Error, invalid move. White move (position, new position):")
#         board = MakeMove(board, whitemove[0], whitemove[1])
#         printboard(board)
#         print "\n", IsPositionUnderThreat(board, 8, 10)
#
#         # print "\n", GetPieceLegalMoves(board, 60)
#         # print InCheck(board, 20)
#
#         board = GenBlackCandidateMoveSimple(board)
#         printboard(board)
#
#         finished = input("\n Done?")
#
# def teststalemate():
#     board = initboard()[2][:]
#     board = GenWhiteCandidateMoveSimple(board)
#     printboard(board)
#
# def testsimple2():
#     board = initboard()[0][:]
#     GenWhiteCandidateMoveSimple2(board)

# testing second algorithm

def testnew():
    board = initboard()[0][:]
    something = GenWhiteCandidateMove(board)
    board = something[0]
    printboard(board)
    somethingelse = GenBlackCandidateMove(board)
    board = somethingelse[0]
    printboard(board)

def testgame():
    board = initboard()[0][:]
    countdown = 10
    while countdown > 0:
        something = GenWhiteCandidateMove(board)
        board = something[0]
        printboard(board)
        print ""
        print "Time elapsed", timeit.default_timer() - start_time,
        somethingelse = GenBlackCandidateMove(board)
        board = somethingelse[0]
        printboard(board)
        print ""
        print "Time elapsed", timeit.default_timer() - start_time,
        countdown -= 1

def testking():
    board = initboard()[0][:]
    printboard(board)
    print(GetPieceLegalMoves(board, 59))


def testCheck():
    #TODO: after alpha beta
    pass

def testPlayer():
    board = initboard()[0][:]
    result = chessPlayer(board, 10)
    print(result[0])
    print("the chosen one")
    print(result[1])
    print("candidates")
    print(result[2])
    print("lvl order")
    print(result[3])
    MakeMove(board, result[1][0][0], result[1][0][1])
    elapsed = timeit.default_timer() - start_time
    print(elapsed)
    result = chessPlayer(board, 20)
    MakeMove(board, result[1][0][0], result[1][0][1])
    printboard(board)
    elapsed = timeit.default_timer() - start_time
    print(elapsed)

def testlegalmoves():
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

    printboard(board0)
    print board0[2]
    moves = GetPieceLegalMoves(board0, 2)
    print moves

def testpos():
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

    pos = GetPlayerPositions(board0)
    print(pos[1])
    print(pos[0])


if __name__ == "__main__":
    # oneplayer()
    # teststalemate()
    # testsimple2()

    # testnew()
    # testking()
    # elapsed = timeit.default_timer() - start_time
    # print(elapsed)
    testgame()
    # testlegalmoves()
    # testpos()

    # testPlayer()

    templist = []
    for i in templist:
        print "hi"

    elapsed = timeit.default_timer() - start_time
    print(elapsed)
