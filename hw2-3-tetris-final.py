#按R重开，分数记录在顶端
#卡耐基梅隆大学 CS15112作业
#部分代码来自课程笔记，请勿用于商业用途。

from tkinter import *
import math
import random
import copy

#got from 15112 notes
#get the cell of a point
def getCell(x, y, data):
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    gridWidth  = data.width - 2*data.marginW
    gridHeight = data.height - 2*data.marginH
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    row = (y - data.marginH) // cellHeight
    col = (x - data.marginW) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)

#got from 15112 notes
#get the bounds of a cell
def getCellBounds(row, col, data):
    gridWidth  = data.width - 2*data.marginW
    gridHeight = data.height - 2*data.marginH
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.marginW + col * columnWidth
    x1 = data.marginW + (col+1) * columnWidth
    y0 = data.marginH + row * rowHeight
    y1 = data.marginH + (row+1) * rowHeight
    return (x0, y0, x1, y1)

#write out the board
def makeBoard():
    oneLine = ["blue","blue","blue","blue","blue",
               "blue","blue","blue","blue","blue"]
    board = []
    for i in range(15):
        Line = copy.copy(oneLine)
        board.append(Line)
    return board

#design the pieces
def makePieces():
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
        [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
        [  True,  True,  True ]]
    oPiece = [[  True,  True ],[  True,  True ]]
    sPiece = [[ False,  True,  True ],
        [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
        [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
        [ False,  True,  True ]]
    return [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]

#determine if a shift is valid
def validShift(data,piece,row,col):
    downReach = col + len(piece)
    rightReach = row + len(piece[0])
    
    for i in range(col, downReach):
        for j in range(row, rightReach):
            if (i >= len(data.board)
                or j >= len(data.board[0])):
                return False
            if(data.board[i][j] != "blue" and
               piece[i-downReach][j-rightReach]):
                return False
    return True

#determine if a rotation is valid
def validRotate(data,piece,currCol,currRow):
   return validShift(data,piece,currRow,currCol)


#rotate a piece
def rotatePiece(data,piece,col,row):
    length = len(piece)
    spread = len(piece[0])
    centerCol = row + spread // 2 
    centerRow = col + length // 2 - 1
    currCol = centerCol
    currRow = centerRow
    currPiece = []
    for i in range(len(piece[0])-1,-1,-1):
        sav = []
        for j in range(len(piece)):
            sav.append(piece[j][i]) #reverse
        currPiece.append(sav)
    if(validRotate(data,currPiece,currCol,currRow)):
        return (currPiece,currRow, currCol)
    return (piece,col,row)
    
#initiation of data
def init(data):
    data.board = makeBoard()
    data.tetrisPieces = makePieces()
    data.rows = 15
    data.cols = 10
    data.marginW = 60
    data.marginH = 10
    data.randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.piecesColors = [ "red", "yellow", "magenta",
                          "pink", "cyan", "green", "orange"]
    data.currPiece =data.tetrisPieces[data.randomIndex]
    data.rowStart = 4
    data.rowEnd = 8
    data.colStart = 0
    data.score = 0
    data.colEnd = 2
    data.isPause = False
    pass

#create a new piece
def generatePiece(data):
    data.rowStart = 4
    data.colStart = -1 #used to avoid margin covering
    data.randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.currPiece = data.tetrisPieces[data.randomIndex]

#check if a piece should stop falling
def checkIfStop(data):
    if(data.colStart >= data.rows - len(data.currPiece)):
        return True
    for i in range(1+data.colStart, 1+data.colStart + len(data.currPiece)):
        for j in range(data.rowStart, data.rowStart + len(data.currPiece[0])):
            if(data.board[i-1][j] != "blue"):
                return True
            if(data.board[i][j] != "blue"
               and data.currPiece[i-1-data.colStart][j-data.rowStart]):
                return True
    return False

#check if game is over
def checkGameOver(data):
    for i in range(len(data.board[0])):
        if(data.board[0][i] != "blue"):
            return True
    return False

#operates when keyboard is pressed
def keyPressed(event, data):
    if(event.char == "r"):
        init(data)
    (row,col) = (data.rowStart,data.colStart)
    piece = []
    if event.keysym == "Up":
        (piece,row,col) = rotatePiece(data,data.currPiece, row,col)
        data.currPiece = copy.copy(piece) #deep copy to avoid multi-changing
    elif event.keysym == "Down":
        col += 1
    elif event.keysym == "Left":
        if(validShift(data,data.currPiece,row-1,col)):
            row -= 1
    elif event.keysym == "Right":
        if(validShift(data,data.currPiece,row+1,col)):
            row += 1
    if(col<0): col = 0
    if(row<0): row = 0
    if(col>data.rows - 1 - len(data.currPiece)):
        col = data.rows - len(data.currPiece)
    if(row>data.cols - 1 - len(data.currPiece[0])):
        row = data.cols - len(data.currPiece[0])
    (data.rowStart,data.colStart) = (row,col)
    pass

#pile up the falling pieces
def placeFallingPiece(data):
    piece = data.currPiece
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            if(i >= data.colStart 
               and j >= data.rowStart
               and i < data.colStart + len(piece)
               and j < data.rowStart + len(piece[0])):
                if(piece[i-data.colStart][j-data.rowStart]):
                    data.board[i][j] = data.piecesColors[data.randomIndex]
    pass

#run on timing 
def timerFired(data):
    data.isPaused = checkGameOver(data)
    data.colStart += 1
    col = data.colStart
    row = data.rowStart
    if(col<0): col = 0
    if(row<0): row = 0
    if(col>data.rows - len(data.currPiece)):
        col = data.rows - len(data.currPiece)
    if(row>data.cols - len(data.currPiece[0])):
        row = data.cols - len(data.currPiece[0])
    (data.colStart,data.rowStart) = col, row
    pass

#draw one cell
def drawCell(data,canvas,x0,x1,y0,y1,row,col,color):
    canvas.create_rectangle(x0, y0, x1, y1, fill=color)
    
def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            drawCell(data,canvas,x0,x1,y0,y1,row,col,data.board[row][col])

#draw a falling piece
def drawFallingPiece(canvas, data):
    currPiece = data.currPiece
    currColor = data.piecesColors[data.randomIndex]
    data.rowEnd = data.rowStart + len(currPiece[0])
    data.colEnd = data.colStart + len(currPiece)
    for col in range(data.rowStart, data.rowEnd):
        for row in range(data.colStart,data.colEnd):
            if(currPiece[row-data.colStart][col-data.rowStart]):
                (x0, y0, x1, y1) = getCellBounds(row, col, data)
                drawCell(data,canvas,x0,x1,y0,y1,row,col,currColor)
    pass

#remove a full row if it is filled with blocks
def removeFullRows(data):
    for i in range(len(data.board)-1,-1,-1):
        checkAll = True
        for j in range(len(data.board[0])):
            if(data.board[i][j] == "blue"):
                checkAll = False
        if(checkAll):
            data.score += 1
            for j in range(len(data.board[0])):
                data.board[i][j] = "blue"
                #paint blue the line itself
            for k in range(i-1,0,-1):
                for j in range(len(data.board[0])):
                    data.board[k+1][j] = data.board[k][j]
                    #down shift the rest
            for j in range(len(data.board[0])):
                data.board[0][j] = "blue"
                #paint the last line

#basic of animation, drawing the scene
def redrawAll(canvas, data):
    data.isPaused = checkGameOver(data)
    drawBoard(canvas, data)
    if(not data.isPaused):
        if(checkIfStop(data)):
            placeFallingPiece(data)
            generatePiece(data)
        drawBoard(canvas, data)
        drawFallingPiece(canvas,data)
        removeFullRows(data)
        canvas.create_text(data.width//2, data.marginH*2,
                           text="Score:"+str(data.score),
                       fill="white", font="Helvetica 14 bold underline")
    else:
        canvas.create_text(data.width//2, data.marginH, text="Game Over!",
                       fill="purple", font="Helvetica 20 bold underline")
    pass

####################################
# use the run function as-is
####################################

def playTetris(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
    

playTetris()
