import freenect
import cv2
import numpy as np

def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return cv2.imwrite('./images/kinectImage.png',array)
   

get_video()