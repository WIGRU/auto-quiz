import cv2
import numpy as np
import configparser



# Import settings
config = configparser.ConfigParser()
config.read('./src/settings.ini')
default = config['DEFAULT']
save_im = default['save_im'] == "True"
out_path = default['out_path']
area_min_limit = float(default['area_min_limit'])
blurValue = int(default['blur'])

def process(imagepath):
    #
    # Mask part of image that will be analyzed
    #

    # Read Image
    image  = cv2.imread(imagepath)

    # To gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur
    blur = cv2.GaussianBlur(gray, (blurValue,blurValue), 0)

    # Adaptive threashhold
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    # find countours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find contours with largest area
    max_area = 0
    c = 0
    for i in contours:
            area = cv2.contourArea(i)
            if area > area_min_limit and area > max_area:
                    max_area = area
                    best_cnt = i
                    image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
            c += 1

    # mask image
    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)

    #
    #   Process image before finding cells
    #
    
    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]

    # thresh
    thresh, img_bin = cv2.threshold(out, 128, 255,cv2.THRESH_BINARY| cv2.THRESH_OTSU)# Invert the image

    img_bin = 255-img_bin 

    # find countours
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if save_im:
        # Draw contours on image
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

        cv2.imwrite(f"{ out_path }1contours.jpg", image)

    return {'contours': contours, 'image': image}