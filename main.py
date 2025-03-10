import time
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)
txt = "Press S to Start"
winTxt = "You won!"
tieTxt = "You tied"
lostTxt = "You lost!"
choices = ["rock.png", "paper.png", "scissors.png"]

startGame = False
showResults = False
endGame = False
computerChoice = -1
win = False
tie = False
lost = False
while True:
    imgBG = cv2.imread("Resources/bg_r.jpg")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    #imgScaled = img[:, 40:280]

    if startGame != True:
        cv2.putText(imgBG,txt, (500, 600), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)

    #Draw hands
    hands, img = detector.findHands(imgScaled)


    if startGame == True:
        if showResults != True:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (500, 600), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)



        if int(timer) > 4 and endGame != True:
            showResults = True
            if hands:
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                print(fingers)

                computerChoice = random.randrange(0, 3)
                endGame = True

                if computerChoice == 0: #If computer chooses rock
                    if fingers == [1,1,1,1,1]:
                        win = True
                    elif fingers == [0,0,0,0,0]:
                        tie = True
                    else:
                        lost = True
                elif computerChoice == 1: #If computer chooses paper
                    if fingers == [0,1,1,0,0]:
                        win = True
                    elif fingers == [1,1,1,1,1]:
                        tie = True
                    else:
                        lost = True
                elif computerChoice == 2: #If computer chooses scissors
                    if fingers == [0,0,0,0,0]:
                        win = True
                    elif fingers == [0,1,1,0,0]:
                        tie = True
                    else:
                        lost = True

                
        if endGame == True:

            choicePic = cv2.imread(str("Resources/" + choices[computerChoice]))

            choicePic = cv2.resize(choicePic, (200, 200))

            x_offset = imgBG.shape[1] - choicePic.shape[1] - 50  # 50px margin from the right
            y_offset = (imgBG.shape[0] - choicePic.shape[0]) // 2  # Center vertically

            imgBG[y_offset:y_offset + choicePic.shape[0], x_offset:x_offset + choicePic.shape[1]] = choicePic

            if win == True:
                cv2.putText(imgBG, winTxt, (500, 600), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
            elif tie == True:
                cv2.putText(imgBG, tieTxt, (500, 600), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
            elif lost == True:
                cv2.putText(imgBG, lostTxt, (500, 600), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)




            #rock = [0,0,0,0,0]
            #paper = [1,1,1,1,1]
            #scissors = [0,1,1,0,0]

















    imgBG[50:470, 20:580] = imgScaled
    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        initialTime = time.time() - 1
        startGame = True

