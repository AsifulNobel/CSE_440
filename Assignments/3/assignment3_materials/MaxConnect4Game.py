#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

from copy import deepcopy
import random
import sys

class maxConnect4Game:
    class GameStateNode:
        """Saves game state in a Node"""

        def __init__(self, state):
            self.state = state
            self.children = [None] * 7
            self.parent = None
            self.last_column_changed = None           # last move

        def has_children(self):
            """Checks if a node is a leaf node"""

            for elem in self.children:
                if elem is not None:
                    return True

            return False

        def value(self, currentTurn):
            """Returns heuristic value of the board state"""
            heuristic_value = 0

            ai_mark = currentTurn
            opponent_mark = currentTurn + 1 if currentTurn == 1 else currentTurn - 1

            # horizontal check
            for row in self.state:
                start_indices = range(4)
                stop_indices = range(4,8)

                for start, stop in zip(start_indices, stop_indices):
                    if row[start:stop] == [ai_mark] * 4:
                        heuristic_value += 1000
                    if row[start:stop-1] == [ai_mark] * 3 and row[stop-1] == [0]:
                        heuristic_value += 400
                    if row[start] == [0] and row[start+1:stop-1] == [ai_mark]:
                        heuristic_value += 400

                    if row[start:stop-2] == [ai_mark] * 2 and row[start+2:stop] == [0] * 2:
                        heuristic_value += 200
                    if row[start] == [0] and row[start+1:stop-1] == [0] * 2 and row[stop-1] == [0]:
                        heuristic_value += 200
                    if row[start:stop-2] == [0] * 2 and row[start+2:stop] == [ai_mark] * 2:
                        heuristic_value += 200

                    if row[start:stop] == [opponent_mark] * 4:
                        heuristic_value -= 1000


            # vertical check
            for column in range(7):
                row_indices = zip(range(0,3), range(1,4), range(2,5), range(3,6))

                for row1, row2, row3, row4 in row_indices:
                    if (self.state[row1][column] == ai_mark and self.state[row2][column] == ai_mark and
                        self.state[row3][column] == ai_mark and self.state[row4][column] == ai_mark):
                        heuristic_value += 1000
                    if (self.state[row1][column] == ai_mark and self.state[row2][column] == ai_mark and
                        self.state[row3][column] == ai_mark and self.state[row4][column] == 0):
                        heuristic_value += 400
                    if (self.state[row1][column] == 0 and self.state[row2][column] == ai_mark
                        and self.state[row3][column] == ai_mark and self.state[row4][column] == ai_mark):
                        heuristic_value += 400

                    if (self.state[row1][column] == ai_mark and self.state[row2][column] == ai_mark and
                        self.state[row3][column] == 0 and self.state[row4][column] == 0):
                        heuristic_value += 200
                    if (self.state[row1][column] == ai_mark and self.state[row2][column] == 0 and
                        self.state[row3][column] == 0 and self.state[row4][column] == ai_mark):
                        heuristic_value += 200
                    if (self.state[row1][column] == 0 and self.state[row2][column] == ai_mark and
                        self.state[row3][column] == ai_mark and self.state[row4][column] == 0):
                        heuristic_value += 200
                    if (self.state[row1][column] == 0 and self.state[row2][column] == ai_mark and
                        self.state[row3][column] == ai_mark and self.state[row4][column] == 0):
                        heuristic_value += 200


                    if (self.state[row1][column] == opponent_mark and self.state[row2][column] == opponent_mark and
                        self.state[row3][column] == opponent_mark and self.state[row4][column] == opponent_mark):
                        heuristic_value -= 1000


            # Check diagonally
            for col1, col2, col3, col4 in zip(range(4), range(1,5), range(2,6), range(3,7)):
                for row1, row2, row3, row4 in zip(range(3), range(1,4), range(2,5), range(3,6)):
                    if (self.state[row1][col1] == ai_mark and self.state[row2][col2] == ai_mark and
                        self.state[row3][col3] == ai_mark and self.state[row4][col4] == ai_mark):
                        heuristic_value += 1000
                    if (self.state[row1][col1] == ai_mark and self.state[row2][col2] == ai_mark and
                        self.state[row3][col3] == ai_mark and self.state[row4][col4] == 0):
                        heuristic_value += 400
                    if (self.state[row1][col1] == 0 and self.state[row2][col2] == ai_mark and
                        self.state[row3][col3] == ai_mark and self.state[row4][col4] == ai_mark):
                        heuristic_value += 400

                    if (self.state[row1][col1] == opponent_mark and self.state[row2][col2] == opponent_mark and
                        self.state[row3][col3] == opponent_mark and self.state[row4][col4] == opponent_mark):
                        heuristic_value -= 1000

            return heuristic_value


    def __init__(self, depth=3):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.depth = depth
        self.emptyColumns = []          # Stores playable columns of the current board state


    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Count the number of playable column
    def checkEmptyColumns(self):
        self.emptyColumns = [index for index, column in enumerate(self.gameBoard[0]) if column==0]

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn+1 if self.currentTurn==1 else self.currentTurn-1))

    # Construct board state from given board state and column input
    def constructState(self, column, game_state_parent, currentTurn):
        for row in range(5, -1, -1):
            # Checks if column is playable
            if not game_state_parent[row][column] in (1, 2):
                game_state_parent[row][column] = currentTurn
                return game_state_parent
        return None

    def populate_state_tree(self, start_node, depth, currentTurn):
        node_game_state = deepcopy(start_node.state)        # deep copy starting board state
        num_children = 7                                    # branching factor
        column = 3                         # starting column for new board state

        for num in range(0, num_children):
            node_game_state = deepcopy(start_node.state)
            changed_child_game_state = self.constructState(column, node_game_state, currentTurn)

            if changed_child_game_state:
                start_node.children[num] = self.GameStateNode(changed_child_game_state)
                start_node.children[num].last_column_changed = column
                start_node.children[num].parent = start_node

            column = column + 1 if column < 6 else 0

        if depth != 0:
            for child_node in start_node.children:
                if child_node:
                    self.populate_state_tree(child_node, depth-1,
                            currentTurn+1 if currentTurn==1 else currentTurn-1)


    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or not node.has_children():
            return node.value(self.currentTurn), node.last_column_changed

        if maximizingPlayer:
            bestValue = float('-inf')
            column = None

            for child_node in node.children:
                if child_node:
                    val, last_column_changed = self.minimax(child_node, depth-1, alpha, beta, False)
                    tmp = bestValue
                    bestValue = max(bestValue, val)

                    if bestValue != tmp and node.parent:
                        column = node.last_column_changed
                    elif bestValue != tmp:
                        column = last_column_changed

                    if bestValue >= beta:
                        return bestValue, column

                    alpha = max(alpha, bestValue)

            return bestValue, column
        else:
            bestValue = float('inf')
            column = None

            for child_node in node.children:
                if child_node:
                    val, last_column_changed = self.minimax(child_node, depth-1, alpha, beta, True)
                    tmp = bestValue
                    bestValue = min(bestValue, val)

                    if bestValue != tmp and node.parent:
                        column = node.last_column_changed
                    elif bestValue != tmp:
                        column = last_column_changed

                    if bestValue <= alpha:
                        return bestValue, column

                    beta = min(beta, bestValue)

            return bestValue, column


    def aiPlay(self):
        start_node = self.GameStateNode(self.gameBoard)

        self.populate_state_tree(start_node, self.depth, self.currentTurn)

        val, column = self.minimax(start_node, self.depth, float('-inf'), float('inf'), True)
        # maximizingPlayer True because computer first, False otherwise

        self.constructState(column, self.gameBoard, self.currentTurn)

        return column

    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0
        self.player2Score = 0

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
