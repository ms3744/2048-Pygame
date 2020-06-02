import random

import numpy as np



# Creates a dummy copy for comparisons
def copyMatrix(matrix):
    copyMat = np.zeros((4, 4))
    np.copyto(copyMat, matrix)
    return copyMat


# creates a matrix and initialises it at two random points
def initialiseMatrix():
    matrix = np.zeros((4, 4))
    dummy = np.ones((4,4))
    generateNew(matrix)
    generateNew(matrix)
    for row in matrix:
        print(row)
    return matrix


# if the values are same they must be added in that direction
# there are 3 main steps to follow the rules
# Step 1: remove all 0s, i.e. all zeroes between the numbers will be removed in that direction
# Step 2: add the equal numbers next to each other, in two steps
# Step 3: remove all 0s again for the final touch
def move(matrix, action):
    score = 0

    copy = copyMatrix(matrix)

    if action.lower() == 'up' or action.lower() == 'down':
        # transpose the matrix to work with rows
        matrix = matrix.T

    # Step 1: eliminate zeroes between
    eliminateZeros(matrix, action)

    # Step 2: add the equal numbers
    col = 0
    for i in range(3):
        for row in range(4):
            if matrix[row][col] == matrix[row][col + 1]:  # they are the same and can be added
                matrix[row][col] += matrix[row][col]
                matrix[row][col + 1] = 0
                # get a score between 0 and 1
                # IDEALLY / 2048
                # BUT FOR TRAINING PURPOSES we let it go to max
                score += matrix[row][col]
        col += 1

    # Step 3: eliminate zeroes between
    eliminateZeros(matrix, action)

    if action.lower() == 'up' or action.lower() == 'down':
        # transpose the matrix back
        matrix = matrix.T

    # first we check if there is any change:
    if np.array_equal(matrix, copy):
        changed = False
    else:
        changed = True

    return score, changed


def eliminateZeros(matrix, action):
    for row in range(4):
        new_row = [x for x in matrix[row] if x != 0]
        length = len(new_row)
        # select padding
        if action.lower() == 'right' or action.lower() == 'down':
            new_row = np.pad(new_row, ((4 - length), 0))
        else:
            new_row = np.pad(new_row, (0, (4 - length)))
        matrix[row] = new_row


def generateNew(matrix):

    # first we have to find an empty box
    # to find that we have to make a list of all empty boxes
    listZeroes = []  # stores the tuple of empty boxes
    possibleBeg = [2, 4]
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == 0:
                listZeroes.append((row, col))

    print(listZeroes)
    if not listZeroes:
        if checkGameOver(matrix):
            return

    # now we choose a random location
    location = random.choice(listZeroes)
    matrix[location[0]][location[1]] = random.choice(possibleBeg)


# checks if the current matrix meets game over condition or not
def checkGameOver(matrix):
    matRight = np.zeros((4, 4))
    matLeft = np.zeros((4, 4))
    matUp = np.zeros((4, 4))
    matDown = np.zeros((4, 4))

    dummy = copyMatrix(matrix)
    _, changedRight = move(dummy, 'right')
    dummy = copyMatrix(matrix)
    _, changedLeft = move(dummy, 'left')
    dummy = copyMatrix(matrix)
    _, changedUp = move(dummy, 'up')
    dummy = copyMatrix(matrix)
    _, changedDown = move(dummy, 'down')

    if not changedDown and not changedLeft and not changedRight and not changedUp:
        return True

    return False
