'''
NOTES:
green = np.uint8([[[0,255,0 ]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print hsv_green

python assembled.py --image images/image_01.png --method "top-to-bottom"

'''

import numpy as np
import argparse
import cv2
import socket
#import freenect

centres = []
instruction = ""
dist_scale = 40
#The bot goes 1/4th meter for 1 sec. We have set least count to 0.5 sec

'''def find_red(image):
	max_red_val = -1
	max_red_px = (-1,-1)
	for c in centres:
		#print c[0],c[1]
		#print "bgr = ",image[c[1]][c[0]]
		red_val = int(image[c[1]][c[0]][2])
		print red_val
		if red_val > max_red_val:
			max_red_val = red_val
			max_red_px = c
	return max_red_px'''
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return cv2.imwrite('./images/kinectImage.png',array)

def hsv(img):
    GREEN_MIN = np.array([32, 0, 0],np.uint8)
    GREEN_MAX = np.array([82, 255, 255],np.uint8)

    RED_MIN = np.array([155, 100, 100],np.uint8)
    RED_MAX = np.array([180, 255, 255],np.uint8)

    BLUE_MIN = np.array([110, 100, 100],np.uint8)
    BLUE_MAX = np.array([130, 255, 255],np.uint8)

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    frame_threshed = cv2.inRange(hsv_img, GREEN_MIN, GREEN_MAX)
    #cv2.imshow('hsvG', frame_threshed)

    frame_threshed = cv2.inRange(hsv_img, RED_MIN, RED_MAX)
    # cv2.imshow('hsvR', frame_threshed)

    frame_threshed = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)
    # cv2.imshow('hsvB', frame_threshed)

def find_red(image, cnts):
    max_red_val = -1
    max_red_px = (-1,-1)
    cnts_count=-1
    for c in cnts:
        cnts_count+=1
        px_count=0
        red_val=0
        x,y,w,h = cv2.boundingRect(c)
        for i in xrange(x,x+w,1):
            for j in xrange(y,y+h,1):
                red_val+= image[j][i][2]
                px_count+=1
        red_val_avg = red_val/px_count
        #print "Avg Red, center = ", red_val_avg, find_center(c)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        if red_val_avg > max_red_val:
            max_red_val = red_val_avg
            max_red_px = find_center(c)
    print "Max red val = ",max_red_val
    print "Max red px = ",max_red_px
    #cv2.imshow("Red Map", image)
    return max_red_px

def find_center(c):
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return ([cX,cY])

def find_black(image, cnts):
    min_red_val = 255
    min_red_px = (-1,-1)
    cnts_count=-1
    for c in cnts:
        cnts_count+=1
        px_count=0
        red_val=0
        x,y,w,h = cv2.boundingRect(c)
        for i in xrange(x,x+w,1):
            for j in xrange(y,y+h,1):
                red_val+= image[j][i][2]
                px_count+=1
        red_val_avg = red_val/px_count
        #print "Avg Red, center = ", red_val_avg, find_center(c)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        if red_val_avg < min_red_val:
            min_red_val = red_val_avg
            min_red_px = find_center(c)
    #print "Max red val = ",max_red_val
    return min_red_px

def draw_contour_box(image, c, i, boundingBoxes):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	centres = []
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	# draw the countour number on the image
	#cv2.putText(image, "#{}".format(i + 1), (cX - dist_scale, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	1.0, (255, 255, 255), 2)

	centres.append((cX, cY))	
	cv2.putText(image, "#{}".format(centres[-1]), (cX - dist_scale, cY - dist_scale), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (255, 255, 255), 1)
	cv2.circle(image, centres[-1], 3, (255, 0, 0), -1)

	#rectangleBox
	
	#box = [np.int0(cv2.cv.BoxPoints(rect2)) for rect2 in boundingBoxes ]
	box = [rect2 for rect2 in boundingBoxes ]
	for b in box:
		#cv2.drawContours(image, [b], -1, (0, 255, 0), 2)
		cv2.rectangle(image,(b[0],b[1]),(b[0]+b[2],b[1]+b[3]),(0,255,0),2)
	


	# return the image with the contour number drawn on it
	return box



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


def draw_contour(image, c, i):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	# draw the countour number on the image
	#cv2.putText(image, "#{}".format(i + 1), (cX - dist_scale, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	1.0, (255, 255, 255), 2)

	centres.append((cX, cY))	
	cv2.putText(image, "#{}".format(centres[-1]), (cX - dist_scale, cY - dist_scale), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (255, 255, 255), 1)
	cv2.circle(image, centres[-1], 3, (255, 0, 0), -1)
	# return the image with the contour number drawn on it
	return image


def drawPlus(arenaMatrix,x,y,w,h):
	for i in xrange(x/dist_scale,(x+w)/dist_scale,1):
		for j in xrange(y/dist_scale,(y+h)/dist_scale,1):
			#print "i and j", i , "  " , j
			arenaMatrix[j][i] = '+'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#host = "192.168.0.102"                          
print "Enter PORT"
port = input()

# connection to hostname on the port.
s.connect(("192.168.0.101", port))  

endreached=False
while(not endreached):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the input image")
    ap.add_argument("-m", "--method", required=True, help="Sorting method")
    args = vars(ap.parse_args())

    # load the image and initialize the accumulated edge image
    #get_video()
    image = cv2.imread("kinectImage.png")
    image_copy = cv2.imread("kinectImage.png")
    accumEdged = np.zeros(image.shape[:2], dtype="uint8")
    height, width, channels = image.shape

    # loop over the blue, green, and red channels, respectively
    for chan in cv2.split(image):
        # blur the channel, extract edges from it, and accumulate the set
        # of edges for the image
        chan = cv2.medianBlur(chan, 11)
        edged = cv2.Canny(chan, 50, 200)
        accumEdged = cv2.bitwise_or(accumEdged, edged)


    #cv2.imshow("Edge Map", accumEdged)

    # find contours in the accumulated image, keeping only the largest
    # ones
    (cnts, _) = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    orig = image.copy()

    # loop over the (unsorted) contours and draw them
    for (i, c) in enumerate(cnts):
        orig = draw_contour(orig, c, i)

    # show the original, unsorted contour image
    #cv2.imshow("Unsorted", orig)

    # sort the contours according to the provided method
    (cnts, boundingBoxes) = sort_contours(cnts, method=args["method"])

    boxes = []
    for (i, c) in enumerate(cnts):
        boxes.append(draw_contour_box(image, c, i, boundingBoxes))

    # loop over the (now sorted) contours and draw them
    for (i, c) in enumerate(cnts):
        draw_contour(image, c, i)


    arenaMatrix = [[' ' for x in xrange(width/dist_scale)] for y in xrange(height/dist_scale)]
    arenaMatrix[0][:] = ['+' for x in xrange(width/dist_scale)] #Setting top row +
    arenaMatrix[height/dist_scale-1][:] = ['+' for x in xrange(width/dist_scale)] #Setting last row +
    for row in arenaMatrix:
        row[0] = '+'
        row[width/dist_scale-1] = '+'


    #print "matrix sizxe = ",len(arenaMatrix[0]), len(arenaMatrix)

    # show the output image
    # cv2.imshow("Sorted", image)
    hsv(image_copy)
    red_center = find_red(image_copy, cnts)
    black_center =find_black(image_copy, cnts)
    print "black center = ",black_center
    cv2.waitKey(0)

    for boxArea in boundingBoxes:   
        x,y,w,h = boxArea
        if(not(red_center[0]/dist_scale in range(x/dist_scale,(x+w)/dist_scale)) or not(red_center[1]/dist_scale) in range(y/dist_scale,(y+h)/dist_scale)):
            if(not(black_center[0]/dist_scale in range(x/dist_scale,(x+w)/dist_scale)) or not(black_center[1]/dist_scale) in range(y/dist_scale,(y+h)/dist_scale)):
                
                drawPlus(arenaMatrix, x, y, w, h)


    arenaMatrix[red_center[1]/dist_scale][red_center[0]/dist_scale] = 'S'
    arenaMatrix[black_center[1]/dist_scale][black_center[0]/dist_scale] = 'E'


    fo = open("maze2.txt", "wb")
    for row in arenaMatrix:
        for ele in row:
            fo.write(ele);
        fo.write('\n')

    # Close opend file
    fo.close()


    '''
    PATH FINDER

    '''

    import Queue


    def intheblock(x,y,lx,ly):
        if x>0 and x<lx and y>0 and y<ly:
            return True
        else:
            return False

    array=[]
    with open("maze2.txt",'r') as f:
        for line in f:
            array.append(line)
    #for a in array:
        #print a
    endx=0
    endy=0
    startx=0
    starty=0
    lx=len(array[0])
    ly=len(array)
    #print lx,ly
    parent=[]
    visited=[]
    for a in xrange(ly):
        parent.append([])
        visited.append([])
        for b in xrange(lx-1):
            if array[a][b]=='E':
                endy=a
                endx=b
            if array[a][b]=='S':
                starty=a
                startx=b
            parent[a].append((0,0))
            visited[a].append(0)


    #print starty,startx
    #print endy,endx


    q=Queue.Queue()
    q.put((starty,startx))
    visited[starty][startx]=1
    parent[starty][startx]=(-1,-1)
    bol=True

    while not q.empty():
        tup=q.get()
        x=tup[1]
        y=tup[0]
        #print tup,parent[y][x]
        if x==endx and y==endy:
            print "path found"
            bol=False
            break
        else:

            # check the above block array[y-1][x]
            if (intheblock(x,y,lx,ly) and (not array[y-1][x]=="+") and (not visited[y-1][x]==1)):
                q.put((y-1,x))
                visited[y-1][x]=1
                parent[y-1][x]=((y,x))
            # check the below block array[y+1][x]
            if (intheblock(x,y,lx,ly) and (not array[y+1][x]=="+") and (not visited[y+1][x]==1)):
                q.put((y+1,x))
                visited[y+1][x]=1
                parent[y+1][x]=((y,x))
            # check the right block array[y][x+1]
            if (intheblock(x,y,lx,ly) and (not array[y][x+1]=="+") and (not visited[y][x+1]==1)):
                q.put((y,x+1))
                visited[y][x+1]=1
                parent[y][x+1]=((y,x))
            # check the left block array[y][x-1]
            if (intheblock(x,y,lx,ly) and (not array[y][x-1]=="+") and (not visited[y][x-1]==1)):
                q.put((y,x-1))
                visited[y][x-1]=1
                parent[y][x-1]=((y,x))

    if not bol:

        tempx=endx
        tempy=endy
        c=0
        path=[]
        while (True):
            t=parent[tempy][tempx]
            #print t
            path.append(t)
            tempy=t[0]
            tempx=t[1]
            c+=1
            if (tempx==startx and tempy==starty):
                break

        path = path[::-1]
        path.append((endy,endx))

        l=len(path)
        finpath=[]
        print "shortest path"
        print "-------------"
        for i in range(1,l):
            cury=path[i][0]
            curx=path[i][1]
            if cury-starty==1:
                finpath.append("down")
            elif cury-starty==-1:
                finpath.append("up")
            elif curx-startx==1:
                finpath.append("right")
            else:
                finpath.append("left")

            starty=cury
            startx=curx
        robfinpath=[]
        ori=1
        for i in finpath:
            if ori==1:
                if i=="up":
                    robfinpath.append('f')
                    ori=1
                elif i=='down':
                    robfinpath.append('b')
                    ori=1
                elif i=='right':
                    robfinpath.append('r')
                    robfinpath.append('f')
                    ori=2
                elif i=='left':
                    robfinpath.append('l')
                    robfinpath.append('f')
                    ori=4

            elif ori==2:
                if i=="up":
                    robfinpath.append('l')
                    robfinpath.append('f')
                    ori=1
                elif i=='down':
                    robfinpath.append('r')
                    robfinpath.append('f')
                    ori=3
                elif i=='right':
                    robfinpath.append('f')
                    ori=2
                elif i=='left':
                    robfinpath.append('b')
                    ori=2


            elif ori==3:
                if i=="up":
                    robfinpath.append('b')
                    ori=3
                elif i=='down':
                    robfinpath.append('f')
                    ori=3
                elif i=='right':
                    robfinpath.append('l')
                    robfinpath.append('f')
                    ori=2
                elif i=='left':
                    robfinpath.append('r')
                    robfinpath.append('f')
                    ori=4

            elif ori==4:
                if i=="up":
                    robfinpath.append('r')
                    robfinpath.append('f')
                    ori=1
                elif i=='down':
                    robfinpath.append('l')
                    robfinpath.append('f')
                    ori=3
                elif i=='right':
                    robfinpath.append('b')
                    ori=4
                elif i=='left':
                    robfinpath.append('f')
                    ori=4
        instruction = "".join(robfinpath)
        print instruction

    if bol:
        print "no path found"


    ''' SOCKET CLIENT '''

    
    print s.recv(1024)                             
    p=instruction[0]                                    
    s.send(p)
    
    print s.recv(1024)

s.close()

