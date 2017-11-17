# USAGE
# python createArena.py --image images/image_01.png --method "top-to-bottom"

# import the necessary packages
import numpy as np
import argparse
import cv2

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0

	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True

	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1

	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))

	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def draw_contour(image, c, i, boundingBoxes):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	centres = []
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	# draw the countour number on the image
	#cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	1.0, (255, 255, 255), 2)

	centres.append((cX, cY))	
	cv2.putText(image, "#{}".format(centres[-1]), (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (255, 255, 255), 1)
	cv2.circle(image, centres[-1], 3, (255, 0, 0), -1)

	#rectangleBox
	
	#box = [np.int0(cv2.cv.BoxPoints(rect2)) for rect2 in boundingBoxes ]
	box = [rect2 for rect2 in boundingBoxes ]
	for b in box:
		#cv2.drawContours(image, [b], -1, (0, 255, 0), 2)
		cv2.rectangle(image,(b[0],b[1]),(b[0]+b[2],b[1]+b[3]),(0,255,0),2)
	


	# return the image with the contour number drawn on it
	return box

def drawPlus(arenaMatrix,x,y,w,h):
	for i in xrange(x/20,(x+w)/20,1):
		for j in xrange(y/20,(y+h)/20,1):
			print "i and j", i , "  " , j
			arenaMatrix[j][i] = '+'


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())

# load the image and initialize the accumulated edge image
image = cv2.imread(args["image"])
height, width, channels = image.shape

accumEdged = np.zeros(image.shape[:2], dtype="uint8")

# loop over the blue, green, and red channels, respectively
for chan in cv2.split(image):
	# blur the channel, extract edges from it, and accumulate the set
	# of edges for the image
	chan = cv2.medianBlur(chan, 11)
	edged = cv2.Canny(chan, 50, 200)
	accumEdged = cv2.bitwise_or(accumEdged, edged)

# show the accumulated edge map
cv2.imshow("Edge Map", accumEdged)

# find contours in the accumulated image, keeping only the largest
# ones
(cnts, _) = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
'''
orig = image.copy()

# loop over the (unsorted) contours and draw them
for (i, c) in enumerate(cnts):
	orig = draw_contour(orig, c, i)

# show the original, unsorted contour image
cv2.imshow("Unsorted", orig)
'''
# sort the contours according to the provided method
(cnts, boundingBoxes) = sort_contours(cnts, method=args["method"])

# loop over the (now sorted) contours and draw them
boxes = []
for (i, c) in enumerate(cnts):
	boxes.append(draw_contour(image, c, i, boundingBoxes))


arenaMatrix = [[' ' for x in xrange(width/20)] for y in xrange(height/20)]
arenaMatrix[0][:] = ['+' for x in xrange(width/20)] #Setting top row +
arenaMatrix[height/20-1][:] = ['+' for x in xrange(width/20)] #Setting last row +
for row in arenaMatrix:
    row[0] = '+'
    row[width/20-1] = '+'

#print boundingBoxes
print "matrix sizxe = ",len(arenaMatrix[0]), len(arenaMatrix)


for boxArea in boundingBoxes:
	print "boxArea = ", boxArea	
	x,y,w,h = boxArea
	print x/20
	print (x+w)/20
	print y/20
	print (y+h)/20

	drawPlus(arenaMatrix,x,y,w,h)
	
fo = open("arena.txt", "wb")
for row in arenaMatrix:
	for ele in row:
		fo.write(ele);
	fo.write('\n')

# Close opend file
fo.close()
# show the output image
cv2.imshow("Sorted", image)
cv2.waitKey(0)