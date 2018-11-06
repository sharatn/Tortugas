#!/usr/bin/env python

import cv2

def is_turtle(contour):
    ### This part needs tuning
    M = cv2.moments(contour);
    return ((M['m00']>1000) and (M['m00']<2000))


if __name__ == "__main__":

    # open the movie
    movie = cv2.VideoCapture('IMG_2371.mov')
    frames = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(movie.get(cv2.CAP_PROP_FPS))
    print("{0} frames at {1} fps".format(frames,fps))

    # create display window
    cv2.namedWindow('turtle',cv2.WINDOW_NORMAL)
    
    for i in range(frames):
        # attempt to read frame
        retval,raw = movie.read()
        if retval:
            blurred = cv2.medianBlur(raw,3)
            
            # turtles appear red so get red channel
            b,g,r = cv2.split(blurred)
            # alternatively use hsv transformation
            #hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

            # threshold - de guessed thresholds until it looked right
            retval,binary = cv2.threshold(r,145,255,cv2.THRESH_BINARY)

            # find contours
            im2,contours,hierarchy = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            gray = cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY)
            
            # select only contours in proper size range
            turtles = filter(is_turtle,contours)
                
            # draw possible turtles as green
            draw = cv2.merge((gray,gray,gray))
            cv2.drawContours(draw,contours,-1,(0,0,255),1)
            cv2.drawContours(draw,turtles,-1,(0,255,0),3)
            
            cv2.imshow('turtle',draw)
            cv2.waitKey(1000/fps)

    # cleanup

    
