import cv2
import time
import random
import numpy as np

top, bottom, right, left = 60, 350, 400, 625  #Rectangle positions
calibrationSetSize = 10   #Number of images are going to be taken to detect gestures. (Higher is more precise but slower.)
sleepTime = 0.5         #The time interval between images when taking photo

rectangleColor = (255, 255, 255) #(B, G, R)
textColor = (255, 255, 255)     #(B, G, R)
textColor2 = (200, 200, 255 )     #(B, G, R)
textColorWinGame = (0, 255, 0)     #(B, G, R)
textColorLoseGame = (0, 0, 255)     #(B, G, R)
rectThickness = 2
recentPlayerMoves = []
fontPlain = cv2.FONT_HERSHEY_PLAIN
fontSimplex = cv2.FONT_HERSHEY_SIMPLEX
threshold = 8 
win = None
game = None
numberWins = 2
#lower_green = np.array([100,100,50])
#upper_green = np.array([255,255,255])

def text(step):    #Different texts for calibration steps. Like switch-case.
            return {
                0: "Place your hands into the rectangle, make a rock move and press space.",
                1: "Make a paper move and press space.",
                2: "Make a scissors move and press space."
            }.get(step, "Text function error")

def calibrate():
    taken = 0
    rockDone = False
    paperDone = False
    scissorsDone = False
    step = 0     #Calibration step status info
    windowTitle = "Calibration - RockPaperScissors"

    print("Calibrating...")
    print("Taking rock pictures...")

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        cv2.rectangle(frame, (left, top), (right, bottom), rectangleColor, rectThickness)
        cv2.putText(frame, "Calibration.", (10, 200), fontSimplex, 2, textColor, 3, cv2.LINE_AA)
        cv2.putText(frame, "Please follow the instruction for calibration.", (20, 230), fontPlain, 1, textColor, 1, cv2.LINE_AA)
        cv2.putText(frame, "Press Esc to return to menu", (20, 250), fontPlain, 1, textColor, 1, cv2.LINE_AA)

        
        cv2.putText(frame, text(step), (1, 400), fontPlain, 1, textColor, 2, cv2.LINE_AA)
        cv2.imshow(windowTitle, frame)

        key = cv2.waitKey(1)

        if key == 27:   #ESC to exit
            break

        elif key == 32:  #Space
            if not rockDone:
                while taken < calibrationSetSize:
                    rectangleArea = frame[top:bottom, right:left]  #Getting the rectangle area of the frame.
                    if(taken == 0):
                        cv2.imwrite("./Rock/" + ".jpg", rectangleArea)
                    rectangleArea = cv2.cvtColor(rectangleArea, cv2.COLOR_BGR2GRAY)
                    #mask = (cv2.inRange(rectangleArea, lower_green, upper_green))
                    #rectangleArea [mask != 0] = [0, 0, 0]
                    cv2.imwrite("./Rock/" + str(taken) + ".jpg", rectangleArea)
                    taken += 1
                    print("Rock picture " + str(taken) + " was taken.")
                    #Refreshing camera frame for taking different photos
                    ret, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    cv2.rectangle(frame, (left, top), (right, bottom), rectangleColor, rectThickness)
                    number_photo = "Saving photo " + str(taken) + " ..."
                    cv2.putText(frame, number_photo, (400, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
                    cv2.imshow(windowTitle, frame)
                    cv2.waitKey(1)
                    time.sleep(sleepTime)   #The time interval between images when taking photo
                rockDone = True
                taken = 0
                print("Rock pictures are ready.")
                print("Taking paper pictures...")
                step += 1
            elif not paperDone:
                while taken < calibrationSetSize:
                    rectangleArea = frame[top:bottom, right:left]  #Getting the rectangle area of the frame.
                    if(taken == 0):
                        cv2.imwrite("./Paper/" + ".jpg", rectangleArea)
                    rectangleArea = cv2.cvtColor(rectangleArea, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite("./Paper/" + str(taken) + ".jpg", rectangleArea)
                    taken += 1
                    print("Paper picture " + str(taken) + " was taken.")
                    #Refreshing camera frame for taking different photos
                    ret, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    cv2.rectangle(frame, (left, top), (right, bottom), rectangleColor, rectThickness)
                    number_photo = "Saving photo " + str(taken) + " ..."
                    cv2.putText(frame, number_photo, (400, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
                    cv2.imshow(windowTitle, frame)
                    cv2.waitKey(1)
                    time.sleep(sleepTime)  #The time interval between images when taking photo
                paperDone = True
                taken = 0
                print("Paper pictures are ready.")
                print("Taking scissors pictures...")
                step += 1
            elif not scissorsDone:
                while taken < calibrationSetSize:
                    rectangleArea = frame[top:bottom, right:left]  #Getting the rectangle area of the frame.
                    if(taken == 0):
                        cv2.imwrite("./Scissors/" + ".jpg", rectangleArea)
                    rectangleArea = cv2.cvtColor(rectangleArea, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite("./Scissors/" + str(taken) + ".jpg", rectangleArea)
                    taken += 1
                    print("Scissors picture " + str(taken) + " was taken.")
                    #Refreshing camera frame for taking different photos
                    ret, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    cv2.rectangle(frame, (left, top), (right, bottom), rectangleColor, rectThickness)
                    number_photo = "Saving photo " + str(taken) + " ..."
                    cv2.putText(frame, number_photo, (400, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
                    cv2.imshow(windowTitle, frame)
                    cv2.waitKey(1)
                    time.sleep(sleepTime)  #The time interval between images when taking photo
                scissorsDone = True
                taken = 0
                print("Scissors pictures are ready.")
                print("Calibration complete")
                break
    cap.release()
    cv2.destroyAllWindows()
    main()

def getMatchScore(frame, imageDir):
    setOfImages = []  #setOfImages from the directory
    comparisonResults = []  #matchTemplate results of each picture
    score = 0         #final match score result
    
    for i in range(calibrationSetSize): #Collecting images as templates
        image = cv2.imread(imageDir + str(i) + ".jpg")
        setOfImages.append(image)

    for template in setOfImages:
        #Slides the template through image and stores comparison result. Comparison method is TM_CCOEFF_NORMED
        comparisonResult = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        comparisonResults.append(comparisonResult)

    for comparisonResult in comparisonResults:
        #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res). max_val is used for TM_CCOEFF_NORMED
        _, max_val, _, _ = cv2.minMaxLoc(comparisonResult)
        score += max_val

    return score

def bestScoreResult(rockScore, paperScore, scissorsScore):
    print(scissorsScore,rockScore,paperScore)
    if(paperScore > threshold or rockScore > threshold or scissorsScore > threshold):
        if (paperScore > rockScore and paperScore > scissorsScore):
            return "Paper"
    
        elif (rockScore > paperScore and rockScore > scissorsScore):
            return "Rock"
    
        elif (scissorsScore > rockScore and scissorsScore > paperScore):
            return "Scissors"
    else:
        return ""

def makeMove():
    global win
# Paper wins by statistics.
# Play scissors or ROCK in the first round. Rock is preferred
# Look for your opponent using the same move twice in a row.
    def make(move):
        if move == "Rock":
            computerMoveImage = cv2.imread("./Rock/.jpg")
            computerMove = "Rock"
        elif move == "Paper":
            computerMoveImage = cv2.imread("./Paper/.jpg")
            computerMove = "Paper"
        elif move == "Scissors":
            computerMoveImage = cv2.imread("./Scissors/.jpg")
            computerMove = "Scissors"
        return computerMoveImage, computerMove

    if len(recentPlayerMoves) == 0:  #First round
        return make("Paper")
    else:  #Other rounds
        chance = round(random.random(), 1)
        if (win == True and chance <0.7):
            if recentPlayerMoves[-1] == "Rock":
                return make("Paper")
            elif recentPlayerMoves[-1] == "Paper":
                return make("Scissors")
            elif recentPlayerMoves[-1] == "Scissors":
                return make("Rock")
        else: 
            if (recentPlayerMoves[-1] == "Rock" and chance < 0.7):
                return make("Scissors")
            elif (recentPlayerMoves[-1] == "Paper" and chance < 0.7):
                return make("Rock")
            elif (recentPlayerMoves[-1] == "Scissors" and chance < 0.7):
                return make("Paper")
            elif (chance >= 0.7 and chance <0.8):
                return make("Rock")
            elif (chance >= 0.8 and chance <0.9):
                return make("Paper")
            elif (chance >= 0.9 and chance <=1):
                return make("Scissors")
        if len(recentPlayerMoves) > 2 and recentPlayerMoves[-1] == recentPlayerMoves[-2] and chance < 0.7:
            if recentPlayerMoves[-1] == "Rock":
                return make("Paper")
            elif recentPlayerMoves[-1] == "Paper":
                return make("Scissors")
            elif recentPlayerMoves[-1] == "Scissors":
                return make("Rock")

def determineWinner(computerMove, playerMove, win, computerScore, playerScore):
    if (playerMove == "Rock" and computerMove == "Scissors"):
        playerScore += 1
        print("Player wins")
        win = True
        print("Computer", computerScore, ":", playerScore, "Player")

    elif (playerMove == "Scissors" and computerMove == "Paper"):
        playerScore += 1
        print("Player wins")
        win = True
        print("Computer", computerScore, ":", playerScore, "Player")

    elif (playerMove == "Paper" and computerMove == "Rock"):
        playerScore += 1
        print("Player wins")
        win = True
        print("Computer", computerScore, ":", playerScore, "Player")

    elif (computerMove == "Rock" and playerMove == "Scissors"):
        computerScore += 1
        print("Computer wins")
        win = False
        print("Computer", computerScore, ":", playerScore, "Player")

    elif (computerMove == "Scissors" and playerMove == "Paper"):
        computerScore += 1
        print("Computer wins")
        win = False
        print("Computer", computerScore, ":", playerScore, "Player")

    elif (computerMove == "Paper" and playerMove == "Rock"):
        computerScore += 1
        print("Computer wins")
        win = False
        print("Computer", computerScore, ":", playerScore, "Player")

    else:
        print("Tie")
        win = None
        print("Computer", computerScore, ":", playerScore, "Player")

    return win, computerScore, playerScore

def play():
    computerMoveImage = cv2.imread("default.jpg")
    computerMove = "Ready"
    computerScore = 0
    playerScore = 0
    global win
    global game
    
    refreshRate = 40  #Detection interval. 40 looks optimal.

    cap = cv2.VideoCapture(0)

    loop = 0           #A variable to create detection intervals
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        cv2.rectangle(frame, (left, top), (right, bottom), rectangleColor, rectThickness)

        if loop % refreshRate == 0:  #Detection interval of a frame.
            rockScore = getMatchScore(frame, "./Rock/")
            paperScore = getMatchScore(frame, "./Paper/")
            scissorsScore = getMatchScore(frame, "./Scissors/")

            playerMove = bestScoreResult(rockScore, paperScore, scissorsScore)

        loop += 1

        statusText = "  Computer     " + str(computerScore) + ":" + str(playerScore) + "      Player"
        cv2.putText(frame, statusText, (50, 50), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
        cv2.putText(frame, computerMove, (80, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
        
        if win == True:
            cv2.putText(frame, "You Win", (270, 400), fontSimplex, 1, (0, 255, 0), 2, cv2.LINE_AA)
        elif win == False:
            cv2.putText(frame, "You Lose", (270, 400), fontSimplex, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Tie", (270, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
        if loop % refreshRate == 0: #When detecting the move for visual feedback
            cv2.putText(frame, "...", (right+100, top+150), fontSimplex, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Detecting...", (440, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, playerMove, (440, 400), fontSimplex, 1, textColor, 2, cv2.LINE_AA)
        cv2.putText(frame, "Press space to play when the computer detects your move correctly", (20, 440), fontPlain, 1, textColor, 1, cv2.LINE_AA)
        cv2.putText(frame, "Press Esc to exit the game", (20, 460), fontPlain, 1, textColor, 1, cv2.LINE_AA)
        #Showing computer's move image
        xOffset=50; yOffset=60
        frame[yOffset:yOffset+computerMoveImage.shape[0], xOffset:xOffset+computerMoveImage.shape[1]] = computerMoveImage

        cv2.imshow("RockPaperScissors", frame)

        key = cv2.waitKey(1)

        if key == 27:   #ESC to exit
            break

        if key == 32:  #Space to make a move
            computerMoveImage, computerMove = makeMove() #Make a move before seeing player's move
            recentPlayerMoves.append(playerMove)
            win, computerScore, playerScore = determineWinner(computerMove, playerMove, win, computerScore, playerScore)
        if(computerScore == numberWins): 
            game = False
            print(game)
            break
        elif(playerScore == numberWins):
            game = True
            print(game)
            break
    cap.release()
    cv2.destroyAllWindows()
    main()
def main():
    
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        cv2.putText(frame, "Press space to play a game.", (20, 230), fontPlain, 1, textColor2, 1, cv2.LINE_AA)
        cv2.putText(frame, "Press Esc to exit the game", (20, 250), fontPlain, 1, textColor2, 1, cv2.LINE_AA)
        cv2.putText(frame, "Press q to calibrate", (20, 270), fontPlain, 1, textColor2, 1, cv2.LINE_AA)
        if(game == True):
            cv2.putText(frame, "You win the game.", (10, 200), fontSimplex, 1, textColorWinGame, 3, cv2.LINE_AA)    
        elif(game == False):
            cv2.putText(frame, "You lose the game.", (10, 200), fontSimplex, 1, textColorLoseGame, 3, cv2.LINE_AA)
        elif(game == None):
            cv2.putText(frame, "Welcome.", (10, 200), fontSimplex, 2, textColor2, 3, cv2.LINE_AA)
        
        key = cv2.waitKey(1)
        
        if key == 27:   #ESC to exit
            break
    
        if key == 32:  #Space to make a move
            play()
            break
        
        if key == 113:  #Del to calibrate
            calibrate()
            break
        cv2.imshow("RockPaperScissors", frame)
    
    cap.release()
    cv2.destroyAllWindows()
main()