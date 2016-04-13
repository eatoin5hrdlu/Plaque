#!C:/cygwin/Python27/python -u
#!/usr/bin/python -u
#!C:/Python27/python -u
# Regions lead with y  (y1,x1,y2,x2) where (y1,x1) is (uppermost,leftmost)
# OpenCV blob,contour algorithms return (X,Y,Width,Height) not(x,y,x2,y2)
#
from __future__ import print_function
import sys, os, time, socket, subprocess, re, traceback
from os  import popen
import glob
import base64, urllib2
from suppress_stdout_stderr import suppress_stdout_stderr
import numpy as np
import cv2
import cv2.cv as cv

def plog(str) :
    print(str, file=sys.stderr)

def nullImage(img, who) :
    if (img == None) :
        plog(who + " called with null image (None)")
        traceback.print_stack()
        return True
    return False


def showUser(img) :
    cv2.imshow("camera", img)
    if cv.WaitKey(100) == 27:
        exit(0)

def contrastThresh(img,iter,mul,off,thresh=127) :
    if (img == None) :
        plog("contrast called with null Image")
    for i in range(iter) :
        plog("Try contrast "+str((iter,mul,off)))
        if (img == None) :
            plog("contrast loop: Image is None")
        else :
            showUser(img)
            img = cv2.add(cv2.multiply(img,mul),off)
            if (img == None) :
                plog( "image(None) after add/mulitply in contrast!")
    showUser(img)
    (ret,img) = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    if (ret == False) :
        plog( "Thresholding failed?")
        img = None
    if (img == None) :
        plog( "img is None after binary threshold in contrast")
    return img

def contrast(img,iter,mul,off) :
    if (img == None) :
        plog("contrast called with null Image")
    for i in range(iter) :
        plog("Try contrast "+str((iter,mul,off)))
        if (img == None) :
            plog("contrast loop: Image is None")
        else :
            showUser(img)
            img = cv2.add(cv2.multiply(img,mul),off)
            if (img == None) :
                plog( "image(None) after add/mulitply in contrast!")
    showUser(img)
    return img



    
# Find settings to find num objects in this image

def countThisMany(img0,num) :
    for clow in [2,4,8] :
        for chigh in [60,80,100] :
            for mul in [1.7,1.8,1.9,2.0] :
                for off in [-70,-80,-90] :
                    img = contrast(img0,1,mul,off)
                    showUser(img)
                    edges = cv2.Canny(img,clow,chigh)
                    contours, _ = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    plog( str(len(contours)) + " contours " + str((clow,chigh,mul,off)))
                    rs = []
                    for c in contours :
                        r = cv2.boundingRect(c)
                        rs.append(r)
                    rs.sort()
                    delta = 1
                    for incr in [1,2,4]:
                        count = 0
                        a = rs[0]
                        for r in rs[1:]:
                            if (    abs(a[0]-r[0]) > incr
                                 or abs(a[1]-r[1]) > incr
                                 or abs(a[2]-r[2]) > incr+delta
                                 or abs(a[3]-r[3]) > incr+delta ) :
                                count = count + 1
                                cv2.rectangle(img,(a[0],a[1]),(a[0]+8,a[1]+8),(200,80,80),2)
                                a = r
                        plog("Counted " + str(count))
                        if ( count == num ) :
                            plog("Nailed it with "+str((clow,chigh,mul,off,incr)))
                            break;
                    showUser(img)
    
        
if __name__ == "__main__" :
    plog("openCV('" + str(cv2.__version__) + "').")
    img = cv2.imread(sys.argv[1])
    plog(str(img.shape))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    countThisMany(gray,161)
