import numpy as np
import cv2


class Player():
    def __init__(self, colours=None):
        self.colours = colours
        self.contoursPoly = None
        self.centers = None
        self.radius = None

    def thresholdImage(self, image, tolerance):
        # Pick Colours
        H = self.colours[0]
        S = self.colours[1]
        V = self.colours[2]
        t = tolerance
            
        # Error Margin = +-m
        m = 35

        # Thresholding HSV image
        Pframe = cv2.inRange(image, (H-t, S-t, V-t), (H+t, S+t, V+t))
        return Pframe

    def findContours(self, frame):
        _, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Approximate contours to polygons + get bounding circles
        self.contoursPoly = [None]*len(contours)
        self.centers = [None]*len(contours)
        self.radius = [None]*len(contours)

        for i, c in enumerate(contours):
            self.contoursPoly[i] = cv2.approxPolyDP(c, 3, True)
            self.centers[i], self.radius[i] = cv2.minEnclosingCircle(self.contoursPoly[i])


    

def chooseColours(HSVframe):
    # Select Region
    r = cv2.selectROI("Pick Colour", HSVframe)
    while sum(r) > 0:     
        # Crop Selection
        selection = HSVframe[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # Average Selection
        a = np.asarray( selection[:,:,:] )
        colours = [int(a[:, :, i].mean()) for i in range(a.shape[-1])]

        cv2.imshow('Pick Colour', HSVframe)
        
        #Break Out
        if (len(colours) > 0):
            cv2.destroyWindow('Pick Colour')
            return colours

def morph(Pframe):
    # Variables
    kernel = np.ones((5,5), np.uint8)
    kernel2 = np.ones((8,8), np.uint8)

    # Morph
    Pframe = cv2.medianBlur(Pframe,5)
    Pframe = cv2.dilate(Pframe, kernel, iterations = 10)
    Pframe = cv2.morphologyEx(Pframe, cv2.MORPH_CLOSE, kernel2)
    Pframe = cv2.morphologyEx(Pframe, cv2.MORPH_OPEN, kernel2)
    Pframe = cv2.medianBlur(Pframe,5)
    return Pframe



def drawContours(frame, p):
    # Draw polygonal contour + circles
    for i in range(len(p.contoursPoly)):
        colour  = p.colours
        cv2.drawContours(frame, p.contoursPoly, i, colour)
        cv2.circle(frame, (int(p.centers[i][0]), int(p.centers[i][1])), int(p.radius[i]), colour, 2)
    return frame

def main():
    Players = []
    # loop over the image paths
    cap = cv2.VideoCapture("squash2.mp4")
    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    success, frame = cap.read()

    # Track 1 or 2 Players
    #raw = input("Enter Number of Players To Track: \n")
    #try:
    #    # Attempt to read user input
    #    noPlayers = int(raw)
    #except:
    #    # Default 1
    #    noPlayers = 1
    noPlayers = 2

    while True:
        success, frame = cap.read()
        if not success: break
        HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
        if len(Players) >= noPlayers:
            for p in Players:
                Pframe = p.thresholdImage(HSVframe, 35)
                Pframe = morph(Pframe)
                p.findContours(Pframe)

                # HeatMap


                # Dev Tracking
                Pframe = drawContours(frame, p)

                # Display to User
                cv2.imshow("Frame", Pframe)
        else:
            colours = chooseColours(HSVframe)
            if colours:
                Players.append(Player(colours))

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
