import cv2
import numpy as np
import  math


#Orginal image
imgdir = 'testcase.jpg'
Orimg = cv2.imread(imgdir)
small = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)
small2 = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)
greysmall = cv2.cvtColor(small,cv2.COLOR_RGB2GRAY)
aftergauss = cv2.GaussianBlur(greysmall,(11,11),0)
#ret,afterthreshold = cv2.threshold(aftergauss, 10, 255, cv2.THRESH_BINARY)

afterthreshold = cv2.adaptiveThreshold(aftergauss,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise = cv2.bitwise_not( afterthreshold);
cv2.imshow("kk",afterbitwise)

torgb = cv2.cvtColor(afterbitwise,cv2.COLOR_GRAY2BGR);
borders = cv2.HoughLinesP(afterbitwise,1, np.pi / 180 ,80,400,10).tolist()
#borders = cv2.HoughLinesP(afterbitwise,1,np.pi/180,275, minLineLength = 600, maxLineGap = 100)[0].tolist()
def ecliduan(x1,x2,y1,y2):
    return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
for line in borders:
    #print ecliduan(line[0][0],line[0][1],line[0][2],line[0][3])
    if (line[0][0] == line[0][2] ) or (line[0][1] == line[0][3] ) :
        cv2.line(small2,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(0,0,255),3,cv2.LINE_AA)
cornerslist = []
for i in xrange(len(borders)):
    for j in range(i+1,len(borders)):
        if ((borders[i][0][0] == borders[i][0][2] ) or (borders[i][0][1] == borders[i][0][3] ))and((borders[j][0][0] == borders[j][0][2] ) or (borders[j][0][1] == borders[j][0][3] )) :
            dist = ((borders[i][0][0]-borders[i][0][2])*(borders[j][0][1]-borders[j][0][3])) - ((borders[i][0][1]-borders[i][0][3])*(borders[j][0][0]-borders[j][0][2]))
            if(dist > 0):
                x1 = borders[i][0][0]
                y1= borders[i][0][1]
                x2 = borders[i][0][2]
                y2 = borders[i][0][3]
                x3 = borders[j][0][0]
                y3= borders[j][0][1]
                x4 = borders[j][0][2]
                y4 = borders[j][0][3]
                x = ((x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)) / dist
                y = ((x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)) / dist
                cornerslist.append([x,y])
print cornerslist

YcornersList = []
XcornerList = []

for corner in cornerslist:
    XcornerList.append(corner[0])
    YcornersList.append(corner[1])
    cv2.circle(small2,(corner[0],corner[1]),2,(255,255,0),2)

XcornerList.sort()
XcornerList.reverse()
YcornersList.sort()
YcornersList.reverse()

Ymaxcorner = max(YcornersList)
Xmaxcorner = max(XcornerList)
Ymincorner = min(YcornersList)
Xmincorner = min(XcornerList)
cv2.circle(small2,(Xmincorner,Ymincorner),2,(255,0,0),2)
cv2.circle(small2,(Xmincorner,Ymaxcorner),2,(255,0,0),2)
cv2.circle(small2,(Xmaxcorner,Ymaxcorner),2,(255,0,0),2)
cv2.circle(small2,(Xmaxcorner,Ymincorner),2,(255,0,0),2)

distofbelowcorner = ecliduan(Xmincorner,Xmaxcorner,Ymaxcorner,Ymaxcorner)
widthOfanswerRow = distofbelowcorner/3
YofcornerOfanswerrow = 0
print YcornersList
for y in range(len(YcornersList)):
    print YcornersList[y]
    if(ecliduan(Xmincorner,Xmincorner,YcornersList[y],Ymaxcorner) > widthOfanswerRow):
        YofcornerOfanswerrow = YcornersList[y]
        break
heightOfanswerRow = YofcornerOfanswerrow - Ymaxcorner

cv2.circle(small2,(Xmaxcorner,YofcornerOfanswerrow),2,(255,0,0),2)
cv2.circle(small2,(Xmincorner,YofcornerOfanswerrow),2,(255,0,0),2)

#Row 1 of Answers
y1row1 = YofcornerOfanswerrow
y2row1 = Ymaxcorner
x1row1 = Xmincorner
x2row1 = Xmincorner + widthOfanswerRow
row1rect = small[y1row1:y2row1, x1row1:x2row1]
cv2.imshow("row1",row1rect)
#Row 2 of Answers
y1row2 = YofcornerOfanswerrow
y2row2 = Ymaxcorner
x1row2 = Xmincorner + widthOfanswerRow
x2row2 = Xmaxcorner - widthOfanswerRow
row2rect = small[y1row2:y2row2, x1row2:x2row2]
cv2.imshow("row2",row2rect)
#Row 3 of Answers
y1row3 = YofcornerOfanswerrow
y2row3 = Ymaxcorner
x1row3 = Xmaxcorner - widthOfanswerRow
x2row3 = Xmaxcorner
row3rect = small[y1row3:y2row3, x1row3:x2row3]
cv2.imshow("row3",row3rect)
#Row of ID
y1row3 = Ymincorner
y2row3 = YofcornerOfanswerrow
x1row3 = Xmaxcorner - widthOfanswerRow
x2row3 = Xmaxcorner
row3rect = small[y1row3:y2row3, x1row3:x2row3]
cv2.imshow("row3",row3rect)

#in Row1
#row1rect = cv2.resize(row1rect, (0,0), fx=2, fy=2)

row1rect = cv2.cvtColor(row1rect,cv2.COLOR_RGB2GRAY)
aftergauss2 = cv2.GaussianBlur(row1rect,(3,3),0)
afterthreshold2 = cv2.adaptiveThreshold(aftergauss2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise2 = cv2.bitwise_not( afterthreshold2);
targets = cv2.HoughCircles(afterbitwise2,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=30,minRadius=0,maxRadius=0)

targets = np.uint16(np.around(targets))
for target in targets[0,:]:
    #by sense the raduises of targets are in between 10 and 15
    print target[2]
    cv2.circle(row1rect,(target[0],target[1]),1,(0,255,0),1)
cv2.imshow("rkkow1",row1rect)








#to get the targets by using hough transform in circle
# targets = cv2.HoughCircles(small,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=30,minRadius=0,maxRadius=0)
#
# targets = np.uint16(np.around(targets))
# locationsoftargets= [] #locatin of x ,y of targets
# numberoftargets = 0 #counter of number of targets
# for target in targets[0,:]:
#     if target[2] < 20:
#         cv2.circle(small2,(target[0],target[1]),2,(0,0,255),3)
cv2.imshow("shouo",afterbitwise)

cv2.imshow("shoo",small2)

cv2.waitKey(0)
cv2.destroyAllWindows()