# x = 434
# y = 250.24
#
# for n in xrange(10):
#     print x - 4 , x + 4
#     x -= 26.25
#For Rotating


import cv2
import numpy as np
import  math


#Orginal image
imgdir = 'testcase.jpg'
Orimg = cv2.imread(imgdir)


small = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)

small2 = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)
small3 = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)

greysmall = cv2.cvtColor(small,cv2.COLOR_RGB2GRAY)
aftergauss = cv2.GaussianBlur(greysmall,(11,11),0)
#ret,afterthreshold = cv2.threshold(aftergauss, 10, 255, cv2.THRESH_BINARY)

afterthreshold = cv2.adaptiveThreshold(aftergauss,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise = cv2.bitwise_not( afterthreshold)
cv2.imshow("kk",afterbitwise)
#Rotate image
kernel_Abig = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(16,16))
erodededtofindrotate = cv2.erode(afterbitwise,kernel_Abig)
cv2.imshow("erodededtofindrotate",erodededtofindrotate)

xyofBigCirles = []
img3,contourssss, hierarchys = cv2.findContours(erodededtofindrotate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourssss:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    print x , y
    cv2.circle(small3,(int(x),int(y)),int(radius),(0,255,255),3)
    xyofBigCirles.append([int(x),int(y)])
angle =  math.atan2((xyofBigCirles[1][1]-xyofBigCirles[0][1]),(xyofBigCirles[1][0]-xyofBigCirles[0][0]))*180/math.pi
print 'angle' , angle
r = cv2.getRotationMatrix2D((small3.shape[0]/2.,small3.shape[0]/2.),angle,1.0)
newimage = cv2.warpAffine(small3,r,(small3.shape[0],small3.shape[0]))
cv2.imshow('newimage',newimage)


cv2.waitKey(0)
cv2.destroyAllWindows()