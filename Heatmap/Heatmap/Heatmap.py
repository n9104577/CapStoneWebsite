import numpy as np
import cv2

# Global
courtPoints = []

class Player():
    def __init__(self, colours=None):
        self.colours = colours
        self.contoursPoly = None
        self.centers = None
        self.radius = None

    # Thresholds the image using the colours picked by the user
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

    # Finds the largest blob available and tracks it
    def findContours(self, frame):
        _, contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area = []
        for contour in contours:
            area.append(cv2.contourArea(contour))
        if area: i = area.index(max(area))

        if area:
            self.contoursPoly = cv2.approxPolyDP(contours[i], 3, True)
            self.centers, self.radius = cv2.minEnclosingCircle(self.contoursPoly)

# Picks a selection of colours and averages it
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

# Uses morphalogical operators to make the blob less pixelated
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

# Draws the tracking circle
def drawContours(frame, p):
    colour = p.colours
    # Draw polygonal contour + circles
    cv2.drawContours(frame, [p.contoursPoly], -1, colour)
    cv2.circle(frame, (int(p.centers[0]), int(p.centers[1])), int(p.radius), colour, 2)
    return frame

# Computes the Homography matrix
def computeHomography(frame, court):
    # Find Court Points
    mask = frame
    while True:
        cv2.imshow('frame', mask)
        cv2.setMouseCallback('frame', on_mouse_click, mask)
        for point in courtPoints:
            cv2.circle(mask, tuple(point), 4, (0,0,255), -1)

        if (cv2.waitKey(1) & 0xFF == ord('q')) or (len(courtPoints) >= 4):
            break
    cv2.destroyWindow('frame')

    height = court.shape[0]
    width = court.shape[1]
    src = np.asarray(courtPoints)

    dst = np.asarray([[0, 0], 
                      [width, 0], 
                      [width, height], 
                      [0, height]])
    #while True:
    #    cv2.imshow('frame', mask)
    #    for point in dst:
    #        cv2.circle(mask, tuple(point), 4, (0,0,255), -1)
    #    if (cv2.waitKey(1) & 0xFF == ord('q')):
    #        break
       
    return cv2.findHomography(src, dst)

def warpFrame(frame, court, h):
    return cv2.warpPerspective(frame, h, (court.shape[1], court.shape[0]))

def warpPoint(point, h):
    p = (point[0], point[1], 1)

    p = np.linalg.inv(h) * p
    p = h * p
    p = p * (1.0 / p[2])

    return p[0], p[1]

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        courtPoints.append([x,y])

def main():
    Players = []
    # loop over the image paths
    cap = cv2.VideoCapture("squash2.mp4")
    court = cv2.imread('court.jpg')

    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    success, frame = cap.read()

    ##Track 1 or 2 Players
    #raw = input("Enter Number of Players To Track: \n")
    #try:
    #    # Attempt to read user input
    #    noPlayers = int(raw)
    #except:
    #    # Default 1
    #    noPlayers = 1
    noPlayers = 1

    h, status = computeHomography(frame, court)

    while True:
        success, frame = cap.read()
        if not success: break
        HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
        if len(Players) >= noPlayers:
            for p in Players:
                Pframe = p.thresholdImage(HSVframe, 35)
                Pframe = morph(Pframe)
                p.findContours(Pframe)
                
                # Dev Tracking
                Pframe = drawContours(frame, p)

                # Warp Frame
                Wframe = warpFrame(frame, court, h)
                wPoint = warpPoint(p.centers, h)
                cv2.circle(Wframe, tuple(wPoint), 4, (0,0,255), -1)


                # HeatMap
                # Display to User
                cv2.imshow("Frame", Pframe)
                cv2.imshow("Warp",  Wframe)
        else:
            colours = chooseColours(HSVframe)
            if colours:
                Players.append(Player(colours))

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
