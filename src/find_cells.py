import cv2
import configparser
import json
import time

config = configparser.ConfigParser()
config.read('./src/settings.ini')
default = config['DEFAULT']

cellarea = json.loads(default['cellarea'])

def find(contours, image):
    c = 0
    count = 0
    cells = []

    for i in contours:
            area = cv2.contourArea(i)
            
            # find center of each cell
            min_area = cellarea["min"]
            max_area = cellarea["max"]

            if min_area < area < max_area:

                    cv2.drawContours(image, contours, c, (0, 0, 255), 2)
                    
                    M = cv2.moments(i)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(image, (cX, cY), 10, (255,0,0), -1)
                    cells.append([cX, cY])
                    
                    count += 1
    
    cv2.imwrite("./out/2cells.jpg", image)

    return {'cells': cells}