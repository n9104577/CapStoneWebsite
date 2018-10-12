import numpy as np
import copy
import cv2
import time

# Global
courtPoints = []

class Player():
    def __init__(self, colours=None):
        self.colours = colours
        self.contoursPoly = None
        self.centers = None
        self.wCenters = None
        self.wCentersList = []
        self.points = []
        self.radius = None
        self.controlPoints = []
        self.distanceTraveled = 0

    # Thresholds the image using the colours picked by the user
    def thresholdImage(self, image, tolerance):
        # Pick Colours
        H = self.colours[0]
        S = self.colours[1]
        V = self.colours[2]
        t = tolerance

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

    def warpPoint(self, h):
        imagepoint = [self.centers[0], self.centers[1], 1]
        worldpoint = np.array(np.dot(h, imagepoint))
        scalar = worldpoint[2]
        xworld = int((worldpoint[0]/scalar))
        yworld = int((worldpoint[1]/scalar))

        height = 200
        x = xworld
        y = yworld + height
        self.wCenters = ((x, y))
        self.wCentersList.append((x, y))

    # get distance as you go
    def getdistanceTraveledAYG(self, court):
        pixPerM = court.shape[0] / 9.75
        
        numCenterPoints = len(self.wCentersList)
        if numCenterPoints > 1:            
            x1 = self.wCentersList[numCenterPoints-2][0]
            y1 = self.wCentersList[numCenterPoints-2][1]
            x2 = self.wCentersList[numCenterPoints-1][0]
            y2 = self.wCentersList[numCenterPoints-1][1]        
            self.distanceTraveled = self.distanceTraveled + (abs(np.sqrt((x2-x1)**2 + (y2-y1)**2))/ pixPerM)
            cv2.line(court, (x1,y1),(x2,y2), (0,0,255), thickness=3, lineType=8, shift=0)
            cv2.imshow("selfDistCourt", court)
        

# Calculate At The End
def getdistanceTraveled(p, court):
        pixPerM = court.shape[0] / 9.75
        distCourt = court
        
        distanceTraveled = 0
        for i in range(0, len(p.wCentersList)-1):
            x1 = p.wCentersList[i][0]
            y1 = p.wCentersList[i][1]
            x2 = p.wCentersList[i+1][0]
            y2 = p.wCentersList[i+1][1]
            distanceTraveled += abs(np.sqrt((x2-x1)**2 + (y2-y1)**2))
            cv2.line(distCourt, (x1,y1),(x2,y2), (0,0,255), thickness=1, lineType=8, shift=0)
            cv2.imshow("distCourt", distCourt)
        distanceTraveled = distanceTraveled/ pixPerM
    
        return distanceTraveled


# find points inside the center T circle
def findControlPoints(p, T_CIRCLE):
    x = p.wCenters[0]
    y = p.wCenters[1]
    if (x - T_CIRCLE[0])**2 + (y - T_CIRCLE[1])**2 < T_CIRCLE[2]**2:
        # inside circle
        p.controlPoints.append(1)
       # cv2.circle(court, (int(x), int(y)), int(5), (0,0,255), thickness=1, lineType=8, shift=0) # remove after testing
    else:
        p.controlPoints.append(0)
       # cv2.circle(court, (int(x), int(y)), int(5), (255,0,0), thickness=1, lineType=8, shift=0) # remove after testing

# Creates Heatmap Kernal
def createKernal(radius):    
    kernal = np.zeros((radius,radius))
    mid = int((radius-1)/ 2)    
    for r in range (1, mid+1, 1):        
        for x in range(0, int(radius/2+0.5)):        
            for y in range(0, radius):
                if (mid-x)**2 + (mid-y)**2 < (abs(mid+1-r))**2:
                    kernal[x][y] = r
                    kernal[radius-1-x][y] = r
    return kernal

# Picks a selection of colours and averages it
def chooseColours(HSVframe):
    # jake for testing so i dont have to repeat
    return [36, 229, 103]
    # Select Region
    r = cv2.selectROI("Pick Colour", HSVframe)
        
    while sum(r) > 0:     
        # Crop Selection
        selection = HSVframe[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # Average Selection
        a = np.asarray( selection[:,:,:] )
        colours = [int(a[:, :, i].mean()) for i in range(a.shape[-1])]

        cv2.imshow('Pick Colour', HSVframe)
        
        # Break Out
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

    #for my vid so i dont have to set them each time
    #courtPoints = [[182, 180], [446, 180], [596, 358], [27, 358]]
    while True:
        cv2.imshow('Pick Points', mask)
        cv2.setMouseCallback('Pick Points', on_mouse_click, mask)
        for point in courtPoints:
            cv2.circle(mask, tuple(point), 4, (0,0,255), -1)
            
        if (cv2.waitKey(1) & 0xFF == ord('q')) or (len(courtPoints) >= 4):
            break
    cv2.destroyWindow('Pick Points')

    height = court.shape[0]
    width = court.shape[1]
    src = np.asarray(courtPoints)

    dst = np.asarray([[0, 0], 
                      [width, 0], 
                      [width, height], 
                      [0, height]])
       
    
    return cv2.findHomography(src, dst)

def genHeatmap(p, accumImage, kernal):
    # Setup Variables
    x = p.wCenters[0]
    y = p.wCenters[1]
    eImg = np.zeros((accumImage.shape[0], accumImage.shape[1]), np.uint8)
    kernal = np.dot(kernal, 5)

    # Left and Top Check
    if (x <= 0) or (y <= 0): return accumImage
    if accumImage.shape[0] - y < 0: return accumImage

    # Bottom and Right Check
    if (x > accumImage.shape[1]- int(np.floor(kernal.shape[1]/2)) -1) or (y > accumImage.shape[0]-int(np.floor(kernal.shape[0]/2)) - 1):
        kernal = kernal[0: accumImage.shape[0]- y, 0: accumImage.shape[1]-x]
        eImg[y - int(np.floor(kernal.shape[0]/2)):y+int(np.floor(kernal.shape[0]/2)) + np.remainder(kernal.shape[0], 2), x - int(np.floor(kernal.shape[1]/2)):x+int(np.floor(kernal.shape[1]/2))+ np.remainder(kernal.shape[1], 2)] = kernal
    # Full Size
    else:
        eImg[y- int(np.floor(kernal.shape[0]/2)):y+int(np.floor(kernal.shape[0]/2))+1, x-int(np.floor(kernal.shape[1]/2)):x+int(np.floor(kernal.shape[1]/2))+1] = kernal
   
    
    eImg = cv2.normalize(eImg, None, 0, 10, cv2.NORM_MINMAX)   
    #accumImage = cv2.add(eImg, accumImage) # For Non-Normalised Image
    accumImage = accumImage.astype(np.int)
    accumImage = eImg + accumImage
    return accumImage

# Track only Court Objects
def setROI(frame):
    # Find x,y,w,h
    x = courtPoints[0][0]
    y = courtPoints[0][1]
    w = courtPoints[1][0] - courtPoints[0][0]
    h = courtPoints[3][1] - courtPoints[0][1]

    # Black out any thing outside of court
    mask = np.zeros(frame.shape,np.uint8)
    mask[y:y+h,x:x+w] = frame[y:y+h,x:x+w]

    return mask
 
def normalize(data):
    data = data.astype(np.float64) / data.max()     # normalize the data to 0 - 1
    data = 255 * data                               # Now scale by 255
    img = data.astype(np.uint8)                     # Convert from float to uint8
    return img

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        courtPoints.append([x,y])

def main():
    Players = []
    # loop over the image paths
    cap = cv2.VideoCapture("squash.mp4")
    court = cv2.imread('court.jpg')
    distTrav = copy.copy(court)

    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    success, frame = cap.read()
    frame = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA)

    noPlayers = 1 # Editable - Change via GUI
    accumImage = np.zeros((court.shape[0], court.shape[1]), np.uint8)
    h, status = computeHomography(frame, court)

    # x, y center points and radius for the 'T' position   T_CIRCLE = [x, y, radius]
    T_CIRCLE = [np.size(court, 1)*.5, np.size(court, 0)*0.56, np.size(court,1)*0.234]
    
    # Dev Circle
    cv2.circle(court, (int(T_CIRCLE[0]), int(T_CIRCLE[1])), int(T_CIRCLE[2]), cv2.COLOR_BGR2HSV, thickness=2, lineType=8, shift=0)
    
    # Create Kernal
    kernal = createKernal(101)
    
    while True:
        success, frame = cap.read()
        if not success: break

        #Image Procssing
        frame = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_AREA)
        cFrame = copy.copy(frame)
        HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if len(Players) >= noPlayers:
            for p in Players:
                Pframe = p.thresholdImage(HSVframe, 35)
                Pframe = morph(Pframe)
                Pframe = setROI(Pframe)
                p.findContours(Pframe)
                
                # Dev Tracking
                Pframe = drawContours(cFrame, p)

                # Warp Frame
                p.warpPoint(h)
                findControlPoints(p, T_CIRCLE)

                # Generate Heatmap and Invert
                accumImage = genHeatmap(p, accumImage, kernal)
                normal = normalize(copy.copy(accumImage))       # Data is copied to preserve int datatype
                normal = cv2.bitwise_not(normal)  
                
                # Add Heatmap to Court
                heatmap = cv2.applyColorMap(normal, cv2.COLORMAP_HOT)
                heatmap = cv2.addWeighted(heatmap, 0.6, court, 0.4, 0)
                
                # Get Distance Travelled
                p.getdistanceTraveledAYG(distTrav)
                
                # HeatMap
                # Display to User
                cv2.imshow("Frame", Pframe)
                cv2.imshow("Warp",  heatmap)
               
                # just to visually check findControlPoints is working
                #cv2.imshow("Court", court)
            
        else:
            colours = chooseColours(HSVframe)
            if colours:
                Players.append(Player(colours))
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # Calculate and print percentage time in center T position
    for p in Players:
        numPoints = len(p.controlPoints)
        numInT = p.controlPoints.count(1)
        per_time = round((numInT / numPoints)*100, 2)
        print("Percentage of Time in T: ", str(per_time) + " %")

        #Bugged Numpy float not callable
        #print("selfdistanceTraveled: ", str(p.distanceTraveled(court)) + " Meters"
if __name__ == "__main__":
    main()
    cv2.waitKey()
    cv2.destroyAllWindows()
