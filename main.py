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
YofcornerOfanswercol = 0
print YcornersList
for y in range(len(YcornersList)):
    print YcornersList[y]
    if(ecliduan(Xmincorner,Xmincorner,YcornersList[y],Ymaxcorner) > widthOfanswerRow):
        YofcornerOfanswercol = YcornersList[y]
        break
heightOfanswerRow = YofcornerOfanswercol - Ymaxcorner

cv2.circle(small2,(Xmaxcorner,YofcornerOfanswercol),2,(255,0,0),2)
cv2.circle(small2,(Xmincorner,YofcornerOfanswercol),2,(255,0,0),2)

#Col 1 of Answers
y1col1 = YofcornerOfanswercol
y2col1 = Ymaxcorner
x1col1 = Xmincorner
x2col1 = Xmincorner + widthOfanswerRow
col1rect = small[y1col1:y2col1, x1col1:x2col1]
cv2.imshow("col1",col1rect)
#Col 2 of Answers
y1col2 = YofcornerOfanswercol
y2col2 = Ymaxcorner
x1col2 = Xmincorner + widthOfanswerRow
x2col2 = Xmaxcorner - widthOfanswerRow
col2rect = small[y1col2:y2col2, x1col2:x2col2]
cv2.imshow("col2",col2rect)
#Col 3 of Answers
y1col3 = YofcornerOfanswercol
y2col3 = Ymaxcorner
x1col3 = Xmaxcorner - widthOfanswerRow
x2col3 = Xmaxcorner
col3rect = small[y1col3:y2col3, x1col3:x2col3]
cv2.imshow("col3",col3rect)
#Col of ID
y1col4 = Ymincorner
y2col4 = YofcornerOfanswercol
x1col4 = Xmaxcorner - widthOfanswerRow
x2col4 = Xmaxcorner
col4rect = small[y1col4:y2col4, x1col4:x2col4]
cv2.imshow("col4",col4rect)

#in Col1
col1rect = cv2.resize(col1rect, (0,0), fx=2, fy=2)

col1rect = cv2.cvtColor(col1rect,cv2.COLOR_RGB2GRAY)
aftergauss2 = cv2.GaussianBlur(col1rect,(3,3),0)
afterthreshold2 = cv2.adaptiveThreshold(aftergauss2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise2 = cv2.bitwise_not( afterthreshold2)
kernel_Abig = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
afterbitwise2 = cv2.erode(afterbitwise2,kernel_Abig)
kernel_Abig1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
afterbitwise2 = cv2.dilate(afterbitwise2,kernel_Abig1)

cv2.imshow("rkkow1th",afterbitwise2)

answersOfcol1XY = []
answersOfcol1 = []

img3,contourss, hierarchys = cv2.findContours(afterbitwise2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    if int(radius) > 5 and int(radius) < 8:
        cv2.circle(col1rect,(int(x),int(y)),3,(0,255,255),3)
        answersOfcol1XY.append([x,y])


cv2.imshow("rkkow1",col1rect)
previousrowY = 522
startpt = 0
row = 16
for answer in xrange(len(answersOfcol1XY) ):
    print answersOfcol1XY[answer][1]
    if(not(answersOfcol1XY[answer][1] > previousrowY - 2 and answersOfcol1XY[answer][1] < previousrowY + 2)):
        startpt += 1
        row -= 1
    if(answersOfcol1XY[answer][0] > 100 and answersOfcol1XY[answer][0] < 103 ):
        answersOfcol1.append([row ,'A'])
    elif(answersOfcol1XY[answer][0] > 131 and answersOfcol1XY[answer][0] < 135 ):
        answersOfcol1.append([row ,'B'])
    elif(answersOfcol1XY[answer][0] > 163 and answersOfcol1XY[answer][0] < 168 ):
        answersOfcol1.append([row ,'C'])
    elif(answersOfcol1XY[answer][0] > 195 and answersOfcol1XY[answer][0] < 200 ):
        answersOfcol1.append([row ,'D'])
    else:
        answersOfcol1.append([row ,'Err'])
    previousrowY = answersOfcol1XY[answer][1]



print answersOfcol1


#in Col2
col2rect = cv2.resize(col2rect, (0,0), fx=2, fy=2)

col2rect = cv2.cvtColor(col2rect,cv2.COLOR_RGB2GRAY)
aftergauss3 = cv2.GaussianBlur(col2rect,(3,3),0)
afterthreshold3 = cv2.adaptiveThreshold(aftergauss3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise3 = cv2.bitwise_not( afterthreshold3)
afterbitwise3 = cv2.erode(afterbitwise3,kernel_Abig)
afterbitwise3 = cv2.dilate(afterbitwise3,kernel_Abig1)

cv2.imshow("rkkow2th",afterbitwise3)

answersOfcol2XY = []
answersOfcol2 = []

img3,contourss2, hierarchys = cv2.findContours(afterbitwise3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss2:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    if int(radius) > 5 and int(radius) < 8:
        print x , y
        cv2.circle(col2rect,(int(x),int(y)),3,(0,255,255),3)
        answersOfcol2XY.append([x,y])


cv2.imshow("rkkow2",col2rect)
previousrowYcol2 = 522
startptcol2 = 0
rowcol2 = 31
for answer in xrange(len(answersOfcol2XY) ):
    print answersOfcol2XY[answer][1]
    if(not(answersOfcol2XY[answer][1] > previousrowYcol2 - 2 and answersOfcol2XY[answer][1] < previousrowYcol2 + 2)):
        startptcol2 += 1
        rowcol2 -= 1
    if(answersOfcol2XY[answer][0] > 93 and answersOfcol2XY[answer][0] < 98 ):
        answersOfcol2.append([rowcol2 ,'A'])
    elif(answersOfcol2XY[answer][0] > 125 and answersOfcol2XY[answer][0] < 132 ):
        answersOfcol2.append([rowcol2 ,'B'])
    elif(answersOfcol2XY[answer][0] > 157 and answersOfcol2XY[answer][0] < 165 ):
        answersOfcol2.append([rowcol2 ,'C'])
    elif(answersOfcol2XY[answer][0] > 191 and answersOfcol2XY[answer][0] < 198 ):
        answersOfcol2.append([rowcol2 ,'D'])
    else:
        answersOfcol2.append([rowcol2 ,'Err'])
    previousrowYcol2 = answersOfcol2XY[answer][1]



print answersOfcol2


#in Col3
col3rect = cv2.resize(col3rect, (0,0), fx=2, fy=2)

col3rect = cv2.cvtColor(col3rect,cv2.COLOR_RGB2GRAY)
aftergauss4 = cv2.GaussianBlur(col3rect,(3,3),0)
afterthreshold4 = cv2.adaptiveThreshold(aftergauss4,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise4 = cv2.bitwise_not( afterthreshold4)
afterbitwise4 = cv2.erode(afterbitwise4,kernel_Abig)
afterbitwise4 = cv2.dilate(afterbitwise4,kernel_Abig1)

cv2.imshow("rkkow3th",afterbitwise4)

answersOfcol3XY = []
answersOfcol3 = []

img3,contourss3, hierarchys = cv2.findContours(afterbitwise4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss3:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    if int(radius) > 5 and int(radius) < 8:
        print x , y
        cv2.circle(col3rect,(int(x),int(y)),3,(0,255,255),3)
        answersOfcol3XY.append([x,y])


cv2.imshow("rkkow3",col3rect)
previousrowYcol3 = 518
startptcol3 = 0
rowcol3 = 46
for answer in xrange(len(answersOfcol3XY) ):
    print answersOfcol3XY[answer][1]
    if(not(answersOfcol3XY[answer][1] > previousrowYcol3 - 2 and answersOfcol3XY[answer][1] < previousrowYcol3 + 2)):
        startptcol3 += 1
        rowcol3 -= 1
    if(answersOfcol3XY[answer][0] > 87 and answersOfcol3XY[answer][0] < 95 ):
        answersOfcol3.append([rowcol3 ,'A'])
    elif(answersOfcol3XY[answer][0] > 120 and answersOfcol3XY[answer][0] < 128 ):
        answersOfcol3.append([rowcol3 ,'B'])
    elif(answersOfcol3XY[answer][0] > 153 and answersOfcol3XY[answer][0] < 161 ):
        answersOfcol3.append([rowcol3 ,'C'])
    elif(answersOfcol3XY[answer][0] > 186 and answersOfcol3XY[answer][0] < 195 ):
        answersOfcol3.append([rowcol3 ,'D'])
    else:
        answersOfcol3.append([rowcol3 ,'Err'])
    previousrowYcol3 = answersOfcol3XY[answer][1]



print answersOfcol3
print '-----'

#Answers
answers= []
answers = answersOfcol3 + answersOfcol2 + answersOfcol1
print answers
finalanswrswithouterr = []
for answer in xrange(len(answers)):
    print answers[answer][1]
    if(not(answers[answer][1] == 'Err')):
        finalanswrswithouterr.append([answers[answer][0],answers[answer][1]])

print finalanswrswithouterr
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