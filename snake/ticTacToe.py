# A 7x7 tictactoe, 4 required for win


def check(board):
    for q in range(7):
        for w in range(7):
            for i in range(3):
                for j in range(2):
                    if i == 2 or j == 1:
                        a = board[q][w]
                        if a != "*":
                            b = True
                            for k in range(4):#tätä vois vissii nopeuttaa
                                if 0 <= q+(i-1)*(k+1) <= 7 and 0 <= w+j*(k+1) <= 7:
                                    if board[q+(i-1)*k][w+j*k] != a:
                                        b = False
                                else:
                                    b = False
                            if b:
                                return a

    return False

def printBoard(board):
    for i in range(7):
        print(board[i][0],board[i][1],board[i][2],board[i][3],board[i][4],board[i][5],board[i][6])

board = []
t = "*"
for i in range(7):
    temp = []
    for j in range(7):
        temp.append(t)
    board.append(temp)

turn = 0
while True:
    printBoard(board)
    a = input("Give square in format [xy]")
    b = int(a[0])
    c = int(a[1])
    if turn % 2 == 0:
        if board[b][c] == "*":
            board[b][c] = "x"
        else:
            turn -= 1
            print("Illegal move")
    else:
        if board[b][c] == "*":
            board[b][c] = "o"
        else:
            turn -= 1
            print("Illegal move")
    d = check(board)
    if d:
        print("winner is " + str(d))
        printBoard(board)
        break
    turn += 1
