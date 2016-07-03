#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

# Extended by Asiful Haque Latif Nobel

import sys
from MaxConnect4Game import *

def checkGameStatus(currentGame):
    currentGame.checkPieceCount()
    
    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'

        currentGame.countScore()

        if currentGame.player1Score > currentGame.player2Score:
            print 'Player 1 won!'
        elif currentGame.player1Score < currentGame.player2Score:
            print 'Player 2 won!'
        else:
            print 'Game Drawn'
        currentGame.printGameBoardToFile()
        currentGame.gameFile.close()
        sys.exit(0)
    else:
        return

def oneMoveGame(currentGame):
    checkGameStatus(currentGame)
    column = currentGame.aiPlay() + 1   # returns the column that is changed

    print 'Game state after move: column', column
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()

def interactiveOneMoveGame(currentGame):
    checkGameStatus(currentGame)

    while True:
        column = int(raw_input('Enter column: ')) - 1

        currentGame.checkEmptyColumns()
        if column in currentGame.emptyColumns:
            break
        else:
            print "Enter a valid column position"

    currentGame.constructState(column, currentGame.gameBoard, currentGame.currentTurn)

    print 'Game state after move: column', column+1
    currentGame.printGameBoard()

    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()

def interactiveGame(currentGame, outFile, depth, turn='computer-next'):
    if turn == 'computer-next':
        oneMoveGame(currentGame)

        while True:
            currentGame.checkPieceCount()
            print "Moves so far:",currentGame.pieceCount

            del currentGame

            currentGame = maxConnect4Game(depth)
            currentGame.gameFile = open(outFile, 'rb')
            file_lines = currentGame.gameFile.readlines()
            currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
            currentGame.currentTurn = int(file_lines[-1][0])
            currentGame.gameFile.close()

            outFile = 'human.txt'
            currentGame.gameFile = open(outFile, 'wb')
            interactiveOneMoveGame(currentGame)

            currentGame.checkPieceCount()
            print "Moves so far:",currentGame.pieceCount

            del currentGame

            currentGame = maxConnect4Game(depth)
            currentGame.gameFile = open(outFile, 'rb')
            file_lines = currentGame.gameFile.readlines()
            currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
            currentGame.currentTurn = int(file_lines[-1][0])
            currentGame.gameFile.close()

            outFile = 'computer.txt'
            currentGame.gameFile = open(outFile, 'wb')
            oneMoveGame(currentGame)
    else:
        interactiveOneMoveGame(currentGame)

        while True:
            currentGame.checkPieceCount()
            print "Moves so far:",currentGame.pieceCount

            del currentGame

            currentGame = maxConnect4Game(depth)
            currentGame.gameFile = open(outFile, 'rb')
            file_lines = currentGame.gameFile.readlines()
            currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
            currentGame.currentTurn = int(file_lines[-1][0])
            currentGame.gameFile.close()

            outFile = 'computer.txt'
            currentGame.gameFile = open(outFile, 'wb')
            oneMoveGame(currentGame)

            currentGame.checkPieceCount()
            print "Moves so far:",currentGame.pieceCount
            del currentGame

            currentGame = maxConnect4Game(depth)
            currentGame.gameFile = open(outFile, 'rb')
            file_lines = currentGame.gameFile.readlines()
            currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
            currentGame.currentTurn = int(file_lines[-1][0])
            currentGame.gameFile.close()

            outFile = 'human.txt'
            currentGame.gameFile = open(outFile, 'wb')
            interactiveOneMoveGame(currentGame)


def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) < 4:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode = argv[1]
    if game_mode == 'interactive':
        inFile, turn = argv[2:4]

        if inFile == 'computer-next' or inFile == 'human-next':
            depth = turn
            turn = inFile
            inFile = None
        else:
            depth = argv[4]

    elif game_mode == 'one-move':
        inFile, outFile, depth = argv[2:5]
    else:
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    depth = int(depth)
    if depth > 6:
        print 'depth should be less than 6, otherwise single move takes more than 30 seconds\n'
        sys.exit(0)

    currentGame = maxConnect4Game(depth) # Create a game

    # Try to open the input file
    if inFile:
        try:
            currentGame.gameFile = open(inFile, 'rb')

            file_lines = currentGame.gameFile.readlines()
            currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
            currentGame.currentTurn = int(file_lines[-1][0])
            currentGame.gameFile.close()
        except IOError:
            sys.exit("\nError opening input file.\nCheck file name.\n")

    # Read the initial game state from the file and save in a 2D list

    print '\nMaxConnect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()

    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if game_mode == 'interactive':
        if turn == 'computer-next':
            outFile = 'computer.txt'
        else:
            outFile = 'human.txt'

        currentGame.gameFile = open(outFile, 'wb')
        interactiveGame(currentGame, outFile, depth, turn)
    else:
        try:
            currentGame.gameFile = open(outFile, 'wb')
        except:
            sys.exit('Error opening output file.')
        oneMoveGame(currentGame) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)
