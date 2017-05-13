"""

Tic - Tac - Toe
Written by: Syed Ali Haider
For CS 100

"""


#######################Imports#############################
import turtle
import random
#######################Setup###############################
turtle.setup(720,720)
#######################Constants###########################
t = turtle.Turtle()
s = turtle.Screen()
s.title("Tic-Tac-Toe")
cellSize = 500
p1Score = p2Score = 0
xTurn = True
playerOne = playerTwo = ""
#######################Shape Functions#####################

def midLine(t,length):
    t.down()
    t.fd(length/2)
    t.back(length)
    t.fd(length/2)
    t.up()
    
def drawX(t,length):
    t.speed(6)
    t.setheading(0)
    t.left(45)
    midLine(t,length)
    t.left(90)
    midLine(t,length)
    t.setheading(0)
    t.up()
    
def drawO(t,diameter):
    t.speed(10)
    t.up()
    t.fd(diameter/2)
    t.down()
    t.left(90)
    t.circle(diameter/2)
    t.up()
    t.setheading(0)
    t.back(diameter/2)

#######################Board Functions##########################
    
def drawBoard(t,cellSize):
    t.speed(10)
    s.bgcolor("beige")
    t.width(15)
    t.up()
    t.fd(cellSize/6)
    t.left(90)
    for i in range(4):
        midLine(t,cellSize)
        t.fd(cellSize/6)
        t.left(90)
        t.fd(cellSize/6)
    t.up()
    k = 0
    for i in range(3):
        for j in range(3):
            t.goto(-cellSize/3 + cellSize/3*j + cellSize*3/23,cellSize/3 - cellSize/3*i+cellSize*3/24)
            t.write(str(k),font = ("Arial",10,"normal"))
            k += 1
    t.home()

#######################Game Supplaments##########################

def dialogue():
    global playerOne, playerTwo

    print("Welcome to Tic Tac Toe")
    mode = input("Would you like to play against a friend or the computer? ")
    playerOne = input("Please enter the name for Player One: ")
    
    if mode[0].lower() == 'c':
        playerTwo = "COMPUTER"
        print("Good Luck")
    else:
        playerTwo = input("Please enter the name for Player Two: ")
    print(playerOne, " will be 'X', and ", playerTwo, "will be 'O'")

def win(t,moves,locations):
    t.color("gold")
    t.speed(6)
    #Horizontal Case
    for i in range(0,9,3):
        if moves[i] == moves[i+1] == moves[i+2]:
            t.goto(locations[i][0] - cellSize/6,locations[i][1])
            t.down()
            t.fd(cellSize)
            return True
    #Vertical Case
    for i in range(3):
        if moves[i] == moves[i+3] == moves[i+6]:
            t.goto(locations[i][0],locations[i][1] + cellSize/6)
            t.right(90)
            t.down()
            t.fd(cellSize)
            return True
    #Diagonal Cases
    if moves[0] == moves[4] == moves[8]:
        t.goto(locations[0][0],locations[0][1])
        t.down()
        t.setheading(315)
        t.back((2*(cellSize/6)**2)**.5)
        t.fd((2*(cellSize)**2)**.5)
        return True
    if moves[2] == moves[4] == moves[6]:
        t.goto(locations[2][0],locations[2][1])
        t.down()
        t.setheading(225)
        t.back((2*(cellSize/6)**2)**.5)
        t.fd((2*(cellSize)**2)**.5)
        return True
    
#########################Computer Functions##########################

def computerTurn(moves):
    winning = [[0,1,2],[3,4,5],[6,7,8],
               [0,3,6],[1,4,7],[2,5,8],
               [0,4,8],[2,4,6]]

    #Attacking Algorithm, Computer to win
    for combo in winning:
        free1 = False
        free2 = False
        remain = combo[0]
        for place in combo:
            if moves[place] == 'O':
                if free1 and moves[place] == 'O':
                    free2 = True
                    continue
                free1 = True
            elif not isValidMove(moves,place):
                break
            else:
                remain = place
        if free1 and free2 and isValidMove(moves,remain):
            return remain

    #Defending Algorithm, PlayerOne to win
    for combo in winning:
        free1 = False
        free2 = False
        remain = combo[0]
        for place in combo:
            if moves[place] == 'X':
                if free1 and moves[place] == 'X':
                    free2 = True
                    continue
                free1 = True
                continue
            elif not isValidMove(moves,place):
                break
            else:
                remain = place
        if free1 and free2 and isValidMove(moves,remain):
            return remain

    #Attacking Algorithm, Computer attempt to chain
    random.shuffle(winning)
    for combo in winning:
        free = False
        remain = combo[0]
        for place in combo:
            if moves[place] == 'O':
                free = True
                continue
            if moves[place] == 'X':
                free = False
                break
            remain = place
        if free and isValidMove(moves,remain):
            return remain

    #Neutral Algorithm, Computer to place move
    keys = list(moves.keys())
    random.shuffle(keys)
    for move in keys:
        if isValidMove(moves,move):
            return move

def isValidMove(moves, move):
    return moves[move] not in "XO"


##########################Game Itself################################

def playTTT(t,cellSize,xTurn):
    drawBoard(t,cellSize)
    playing = True
    global p1Score
    global p2Score

    #Determining locations
    moves = {}
    locations = {}
    k = 0
    for i in range(3):
        for j in range(3):
            locations[k] = (-cellSize/3 + cellSize/3*j,cellSize/3 - cellSize/3*i)
            moves[k] = str(k)
            k += 1

    while playing:
        while True:
            try:
                if xTurn:
                    print(playerOne + " to move")
                    move = int(input("Please enter a space to move, 0 - 8: "))
                else:
                    print(playerTwo + " to move")
                    if playerTwo == "COMPUTER":
                        move = computerTurn(moves)
                    else:
                        move = int(input("Please enter a space to move, 0 - 8: "))
                break
            except ValueError:
                print("Not a valid number, please try again!")
                
        if 0 <= move <= 8 and moves[move] not in "XO":
            t.goto(locations[move][0],locations[move][1])
            
            if xTurn:
                t.color("red")
                drawX(t,cellSize/3)
                xTurn = False
                moves[move] = 'X'
            else:
                t.color("blue")
                drawO(t,cellSize/4)
                xTurn = True
                moves[move] = 'O'
                
        else:
            print("Error, please enter a valid space")
            continue

        if win(t,moves,locations):
            if xTurn:
                print(playerTwo + " wins!")
                p2Score += 1
            else:
                print(playerOne + " wins!")
                p1Score += 1
            break
        
        playing = False
        for value in moves.values():
            if value not in "XO":
                playing = True

    
    print(playerOne + "'s score: " + str(p1Score))
    print(playerTwo + "'s score: " + str(p2Score))
    
    rematch = input("Game Over! Would you like to play again? ")
    
    if rematch[0].lower() == 'y':
        s.reset()
        playTTT(t,cellSize,xTurn)
    else:
        print("Good Match, have a nice day!")
        s.bye()


if __name__ == "__main__":
    dialogue()
    playTTT(t,cellSize,xTurn)







        
