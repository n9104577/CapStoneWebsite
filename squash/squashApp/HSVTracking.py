import cv2
import time
import numpy as np
from squashApp.models import Video
def chooseColours(HSVframe):
    # Select Region
    r = cv2.selectROI("Pick Colour", HSVframe)
    while sum(r) > 0:     
        # Crop Selection
        selection = HSVframe[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # Average Selection
        a = np.asarray( selection[:,:,:] )
        colours = [int(a[:, :, i].mean()) for i in range(a.shape[-1])]
        print(colours)
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

def findContours(Pframe, frame):
    _, contours, hierarchy = cv2.findContours(Pframe, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate contours to polygons + get bounding rects and circles
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
    
    #Show Just Boundry
    #Pframe = np.zeros((Pframe.shape[0], Pframe.shape[1], 3), dtype=np.uint8)

    # Draw polygonal contour + bonding rects + circles
    for i in range(len(contours)):
        color = (0, 255, 0)
        cv2.drawContours(frame, contours_poly, i, color)
        cv2.circle(frame, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

    # Return Frame
    return frame, Pframe

def main(fileName):
	colours = []
	# loop over the image paths
	cap = cv2.VideoCapture(fileName)

	# cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FPS, 60)
	success, frame = cap.read()

	# Get current width of frame
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
	# Define the codec and create VideoWriter object
	
	out = cv2.VideoWriter('media/test.mp4',-1, 20.0, (int(width),int(height)))
	while True:
		success, frame = cap.read()
		if not success: break
		HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		if colours:
			# Pick Colours
			H = colours[0]
			S = colours[1]
			V = colours[2]

			# Error Margin = +-m
			m = 35
			# Thresholding HSV image
			Pframe = cv2.inRange(HSVframe, (H-m, S-m, V-m), (H+m, S+m, V+m))

			Pframe = morph(Pframe)
			Pframe, mask = findContours(Pframe, frame)
			# Saves for video
			out.write(Pframe)
			cv2.imshow("Frame", Pframe)
			#cv2.imshow("mask", mask)
			print("processing")
		else:
			colours = [37, 208, 107]

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	out.release()
	data = {'name' : 'test.mp4', 'videofile' : 'test.mp4'}
	Video.objects.create(**data)
	print("done")

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
