from datetime import datetime

def solve(count):
    if count == 81:
        print(datetime.now() - start)
        print(board)
        return True
    else:
        poss, row, column = get_best()
        poss = sorted(poss)
        for digit in poss:
            board[row][column] = digit
            dead, removed = dead_end(row, column, digit)
            if not dead:
                solved = solve(count + 1)
                if solved:
                    return True
            for entry in removed:
                    if not digit in poss_dict[entry]: #syntax?
                        poss_dict[entry].append(digit)
        board[row][column] = 0
        count -= 1
        return False

def dead_end(row, column, value): #update poss, return whether dead_end
    dead_end = False
    #test square
    removed = []
    square_row = (row//3) * 3
    square_column = (column//3) * 3
    for i in range(2, -1 ,-1):
        for j in range (2, -1 ,-1):
            if value in poss_dict[(square_row + i, square_column + j)]:
                poss_dict[(square_row + i, square_column + j)].remove(value)
                removed.append((square_row + i, square_column + j))
            if len(poss_dict[(square_row + i, square_column + j)]) == 0 and board[square_row + i][square_column + j] == 0:
                dead_end = True
    #test row
    for i in range(8, -1 ,-1):
        if value in poss_dict[(row,i)]:
                poss_dict[(row,i)].remove(value)
                removed.append((row,i))
        if len(poss_dict[(row,i)]) == 0 and board[row][i] == 0:
                dead_end = True
    #test column
    for i in range(8, -1 ,-1):
        if value in poss_dict[(i,column)]:
                poss_dict[(i,column)].remove(value)
                removed.append((i,column))
        if len(poss_dict[(i,column)]) == 0 and board[i][column] == 0:
                dead_end = True

    return dead_end, removed

def get_poss(row, column):#return list of possible digits
    if not board[row][column] == 0:
        return []
    row_digits = board[row]
    column_digits = []
    for i in range(0 ,9):
        column_digits.append(board[i][column])
    square_digits = get_square(row, column)
    
    all_digits = row_digits + column_digits + square_digits
    poss = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range (1, 10):
        if i in all_digits:
            poss.remove(i)
    return poss

def get_square(row, column):
    square = []
    row = (row//3) * 3
    column = (column//3) * 3
    for i in range(2, -1 ,-1):
        for j in range (2, -1 ,-1):
            square.append(board[row + i][column + j])
    return square

def get_count(): # return row and column of next square to check
    count = 81
    for row in range(8, -1 ,-1):
        for column in range(8, -1 ,-1):
            if board[row][column] == 0:
                count -= 1
    return count

def get_best(): #return list of poss digits, row and column int
    min = 9
    best_poss, best_row, best_column = None, None, None
    if (datetime.now() - start).seconds > 1:
        r = second_range
    else:
        r = first_range
    for row in r:
        for column in r:
            poss = poss_dict[(row, column)]
            if len(poss) < min and board[row][column] == 0:
                best_poss = poss
                best_row = row
                best_column = column
                if len(poss) == 1:
                    return poss, row, column
    return best_poss, best_row, best_column

def get_puzzles():
    puzzles = []
    with open('sudoku95.txt') as file:
        for x in range(95):
            current = file.readline()
            puzzle = []
            for i in range(9):
                puzzle.append([])
                for j in range(9):
                    if current[j + 9 * i] == '.':
                        puzzle[i].append(0)    
                    else:
                        puzzle[i].append(int(current[j + 9 * i]))
            puzzles.append(puzzle)
    print("Finished processing puzzles")
    return puzzles

def build_possible():
    possible = {}
    for row in range(9):
        for column in range(9):
            possible[(row, column)] = get_poss(row, column)
    return possible


puzzles = get_puzzles()
puzzle_number = 1
board = []
first_range = [8, 7, 6, 5, 4, 3, 2, 1, 0]
second_range = [0, 1, 2, 3, 4, 5, 6, 7, 8]
total_start = datetime.now()
for puzzle in puzzles:
    print('#', puzzle_number)
    board = puzzle
    poss_dict = {}
    poss_dict = build_possible()
    count = get_count()
    start = datetime.now()
    solve(count)
    solved = False
    puzzle_number += 1
print(datetime.now() - total_start)

##
##RECORD TIME::::::
##0:03:15.675316
##
