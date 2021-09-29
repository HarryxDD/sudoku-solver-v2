def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return(i, j)
    return None


def is_valid(board, num, pos):
    # Check row
    if num in board[pos[0]]:
        return False 

    # Check column
    if num in [board[i][pos[1]] for i in range(len(board))]:
        return False

    # Check the square
    row_x = (pos[0] // 3) * 3
    col_x = (pos[1] // 3) * 3
    for i in range(row_x, row_x + 3):
        for j in range(col_x, col_x + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
                
    return True


def solve_sud(board):
    check = find_empty(board)
    if check is None:
        return True
    else:
        row, col = check
    for num in range(1,10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sud(board):
                return True
            board[row][col] = 0
    return False


##################################################