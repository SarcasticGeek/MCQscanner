"""
Author: Mohamed Essam Fathalla Mohamed
mail: mohamedessamfathalla@gmail.com
Title: MCQ scanner
"""
import cv2
import numpy as np
import  math


#Orginal image
imgdir = 'testcases/test3.jpg'
Orimg = cv2.imread(imgdir)


small = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)

small2 = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)
small3 = cv2.resize(Orimg, (0,0), fx=0.4, fy=0.4)

greysmall = cv2.cvtColor(small,cv2.COLOR_RGB2GRAY)
aftergauss = cv2.GaussianBlur(greysmall,(11,11),0)
#ret,afterthreshold = cv2.threshold(aftergauss, 10, 255, cv2.THRESH_BINARY)

afterthreshold = cv2.adaptiveThreshold(aftergauss,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise = cv2.bitwise_not( afterthreshold)
cv2.imshow("1_afterthreshold",afterbitwise)
cv2.imwrite("dist/1_afterthreshold.jpg",afterbitwise)
#Rotate image
kernel_Abig = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(18,18))
erodededtofindrotate = cv2.erode(afterbitwise,kernel_Abig)
cv2.imshow("2_erodededtofindrotate",erodededtofindrotate)
cv2.imwrite("dist/2_erodededtofindrotate.jpg",erodededtofindrotate)

xyofBigCirles = []
img3,contourssss, hierarchys = cv2.findContours(erodededtofindrotate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourssss:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    print "xyofBigCirles", x , y
    cv2.circle(small3,(int(x),int(y)),int(radius),(0,255,255),3)
    xyofBigCirles.append([int(x),int(y)])
angle =  math.atan2((xyofBigCirles[1][1]-xyofBigCirles[0][1]),(xyofBigCirles[1][0]-xyofBigCirles[0][0]))*180/math.pi
print 'angle1' , angle

#if image overturned
if(xyofBigCirles[0][1] < erodededtofindrotate.shape[1] and  xyofBigCirles[1][1] < erodededtofindrotate.shape[1] ):
    angle = 180 + angle

if(angle <= -90.0):
 angle = 180.0 + angle

if(angle == 180.0):
 angle = 0

print 'angle' , angle
r = cv2.getRotationMatrix2D((small3.shape[0]/2.,small3.shape[0]/2.),angle,1.0)
newimage = cv2.warpAffine(small3,r,(small3.shape[0],small3.shape[0]))
#newimage = cv2.resize(newimage,(small.shape[0],small.shape[1]),0,0,cv2.INTER_NEAREST)
small3 = cv2.warpAffine(small3,r,(small3.shape[0],small3.shape[0]))
small2 = cv2.warpAffine(small2,r,(small3.shape[0],small3.shape[0]))
small = cv2.warpAffine(small,r,(small3.shape[0],small3.shape[0]))
erodededtofindrotate = cv2.warpAffine(erodededtofindrotate,r,(erodededtofindrotate.shape[0],erodededtofindrotate.shape[0]))


afterbitwise = cv2.warpAffine(afterbitwise,r,(small3.shape[0],small3.shape[0]))

cv2.imshow('3_imageafterrotating',newimage)
cv2.imwrite("dist/3_imageafterrotating.jpg",newimage)

cv2.imshow('4_afterbitwise_imageafterrotating',afterbitwise)
cv2.imwrite("dist/4_afterbitwise_imageafterrotating.jpg",afterbitwise)


#Translation image to pointX,Y reference xyofBigCirles 88.5208358765 617.958312988
xyofBigCirles = []
img3,contourssssd, hierarchys = cv2.findContours(erodededtofindrotate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourssssd:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    print "newxyofBigCirles", x , y
    cv2.circle(small3,(int(x),int(y)),int(radius),(0,255,255),3)
    xyofBigCirles.append([int(x),int(y)])

def translateimage(imgorginal,Tx,Ty):
    #rows,cols = imgorginal.shape
    M = np.float32([[1,0,Tx],[0,1,Ty]])
    dst = cv2.warpAffine(imgorginal,M,(imgorginal.shape[0],imgorginal.shape[1]))
    return dst
#Sort xyofBigCirles
xyofBigCirles = sorted(xyofBigCirles,key=lambda l:l[0])
xyofBigCirles.reverse()

small3 = translateimage(small3,88.5208358765-xyofBigCirles[1][0],617.958312988-xyofBigCirles[1][1])
small2 = translateimage(small2,88.5208358765-xyofBigCirles[1][0],617.958312988-xyofBigCirles[1][1])
small = translateimage(small,88.5208358765-xyofBigCirles[1][0],617.958312988-xyofBigCirles[1][1])
afterbitwise = translateimage(afterbitwise,88.5208358765-xyofBigCirles[1][0],617.958312988-xyofBigCirles[1][1])

#Hough Lines
torgb = cv2.cvtColor(afterbitwise,cv2.COLOR_GRAY2BGR)
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

Ymaxcorner =  577
print "Ymax", max(YcornersList) #
Xmaxcorner = 438
print "Xmax", max(XcornerList) #
Ymincorner = 45
print "Ymin", min(YcornersList) #
Xmincorner = 40
print "Xmin", min(XcornerList) #

cv2.circle(small2,(Xmincorner,Ymincorner),2,(255,0,255),2)
cv2.circle(small2,(Xmincorner,Ymaxcorner),2,(255,0,255),2)
cv2.circle(small2,(Xmaxcorner,Ymaxcorner),2,(255,0,255),2)
cv2.circle(small2,(Xmaxcorner,Ymincorner),2,(255,0,255),2)

distofbelowcorner = ecliduan(Xmincorner,Xmaxcorner,Ymaxcorner,Ymaxcorner)
widthOfanswerRow = distofbelowcorner/3
YofcornerOfanswercol = 0
for y in range(len(YcornersList)):
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
cv2.imshow("5_Col1ofAnswers",col1rect)
cv2.imwrite("dist/5_Col1ofAnswers.jpg",col1rect)

#Col 2 of Answers
y1col2 = YofcornerOfanswercol
y2col2 = Ymaxcorner
x1col2 = Xmincorner + widthOfanswerRow
x2col2 = Xmaxcorner - widthOfanswerRow
col2rect = small[y1col2:y2col2, x1col2:x2col2]
cv2.imshow("6_Col2ofAnswers",col2rect)
cv2.imwrite("dist/6_Col2ofAnswers.jpg",col2rect)

#Col 3 of Answers
y1col3 = YofcornerOfanswercol
y2col3 = Ymaxcorner
x1col3 = Xmaxcorner - widthOfanswerRow
x2col3 = Xmaxcorner
col3rect = small[y1col3:y2col3, x1col3:x2col3]
cv2.imshow("7_Col3ofAnswers",col3rect)
cv2.imwrite("dist/7_Col3ofAnswers.jpg",col3rect)

#Col of ID
y1col4 = Ymincorner
y2col4 = YofcornerOfanswercol
x1col4 = Xmaxcorner - widthOfanswerRow
x2col4 = Xmaxcorner
col4rect = small[y1col4:y2col4, x1col4:x2col4]
cv2.imshow("8_ColIDofAnswers",col4rect)
cv2.imwrite("dist/8_ColIDofAnswers.jpg",col4rect)

#in Col1
col1rect = cv2.resize(col1rect, (0,0), fx=2, fy=2)
col1rect = cv2.cvtColor(col1rect,cv2.COLOR_RGB2GRAY)
col1rectcopy = col1rect.copy()
aftergauss2 = cv2.GaussianBlur(col1rect,(3,3),0)
afterthreshold2 = cv2.adaptiveThreshold(aftergauss2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10)

afterbitwise2 = cv2.bitwise_not( afterthreshold2)

kernel_Abig = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
afterbitwise2 = cv2.erode(afterbitwise2,kernel_Abig)
kernel_Abig1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
afterbitwise2 = cv2.dilate(afterbitwise2,kernel_Abig1)
cv2.imshow("9_ThresholdCol1ofAnswers",afterbitwise2)
cv2.imwrite("dist/9_ThresholdCol1ofAnswers.jpg",afterbitwise2)

answersOfcol1XY = []
answersOfcol1 = []
for drawcirclie in range(102,551,32):
    print drawcirclie
    cv2.circle(afterbitwise2,(220,drawcirclie),6,(255,255,255),1)

cv2.imshow("demo",afterbitwise2)

img3,contourss, hierarchys = cv2.findContours(afterbitwise2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    print "coldd" , col1rect[int(y),int(x)]
    if int(radius) > 5 and int(radius) < 8 and col1rect[int(y),int(x)] < 215:

        cv2.circle(col1rect,(int(x),int(y)),3,(0,255,255),3)
        answersOfcol1XY.append([x,y])


cv2.imshow("10_ThresholdCol1ofAnswersDetectAnswers",col1rect)
cv2.imwrite("dist/10_ThresholdCol1ofAnswersDetectAnswers.jpg",col1rect)

previousrowY = 522
startpt = 0
row = 16
print "answersOfcol1XY" ,answersOfcol1XY
for answer in xrange(len(answersOfcol1XY) ):
    if(answersOfcol1XY[answer][1] > 60 ):
        if(not(answersOfcol1XY[answer][1] > previousrowY - 5 and answersOfcol1XY[answer][1] < previousrowY + 5)):
            startpt += 1
            row -= 1
        if(answersOfcol1XY[answer][0] > 98 and answersOfcol1XY[answer][0] < 109 ):
            answersOfcol1.append([row ,'A'])
        elif(answersOfcol1XY[answer][0] > 126 and answersOfcol1XY[answer][0] < 138 ):
            answersOfcol1.append([row ,'B'])
        elif(answersOfcol1XY[answer][0] > 163 and answersOfcol1XY[answer][0] < 170 ):
            answersOfcol1.append([row ,'C'])
        elif(answersOfcol1XY[answer][0] > 195 and answersOfcol1XY[answer][0] < 205 ):
            answersOfcol1.append([row ,'D'])
        else:
            answersOfcol1.append([row ,'Err'])
        previousrowY = answersOfcol1XY[answer][1]





#in Col2
col2rect = cv2.resize(col2rect, (0,0), fx=2, fy=2)

col2rect = cv2.cvtColor(col2rect,cv2.COLOR_RGB2GRAY)
aftergauss3 = cv2.GaussianBlur(col2rect,(3,3),0)
afterthreshold3 = cv2.adaptiveThreshold(aftergauss3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise3 = cv2.bitwise_not( afterthreshold3)
afterbitwise3 = cv2.erode(afterbitwise3,kernel_Abig)
afterbitwise3 = cv2.dilate(afterbitwise3,kernel_Abig1)

cv2.imshow("11_ThresholdCol2ofAnswers",afterbitwise3)
cv2.imwrite("dist/11_ThresholdCol2ofAnswers.jpg",afterbitwise3)


answersOfcol2XY = []
answersOfcol2 = []
for drawcirclie in range(102,551,32):
    print drawcirclie
    cv2.circle(afterbitwise3,(220,drawcirclie),6,(255,255,255),1)

img3,contourss2, hierarchys = cv2.findContours(afterbitwise3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss2:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    if int(radius) > 5 and int(radius) < 8 and col2rect[int(y),int(x)] < 215:
        print "cold" , col2rect[int(y),int(x)]
        cv2.circle(col2rect,(int(x),int(y)),3,(0,255,255),3)
        answersOfcol2XY.append([x,y])


cv2.imshow("12_ThresholdCol2ofAnswersDetectAnswers",col2rect)
cv2.imwrite("dist/12_ThresholdCol2ofAnswersDetectAnswers.jpg",col2rect)

previousrowYcol2 = 522
startptcol2 = 0
rowcol2 = 31
print "answersOfcol2XY" , answersOfcol2XY
for answer in xrange(len(answersOfcol2XY) ):
    if(answersOfcol2XY[answer][1] > 60 ):
        if(not(answersOfcol2XY[answer][1] > previousrowYcol2 - 4 and answersOfcol2XY[answer][1] < previousrowYcol2 + 4)):
            startptcol2 += 1
            rowcol2 -= 1
        if(answersOfcol2XY[answer][0] > 90 and answersOfcol2XY[answer][0] < 105 ):
            answersOfcol2.append([rowcol2 ,'A'])
        elif(answersOfcol2XY[answer][0] > 125 and answersOfcol2XY[answer][0] < 137 ):
            answersOfcol2.append([rowcol2 ,'B'])
        elif(answersOfcol2XY[answer][0] > 157 and answersOfcol2XY[answer][0] < 170 ):
            answersOfcol2.append([rowcol2 ,'C'])
        elif(answersOfcol2XY[answer][0] > 191 and answersOfcol2XY[answer][0] < 200 ):
            answersOfcol2.append([rowcol2 ,'D'])
        else:
            answersOfcol2.append([rowcol2 ,'Err'])
        previousrowYcol2 = answersOfcol2XY[answer][1]





#in Col3
col3rect = cv2.resize(col3rect, (0,0), fx=2, fy=2)

col3rect = cv2.cvtColor(col3rect,cv2.COLOR_RGB2GRAY)
aftergauss4 = cv2.GaussianBlur(col3rect,(3,3),0)
afterthreshold4 = cv2.adaptiveThreshold(aftergauss4,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise4 = cv2.bitwise_not( afterthreshold4)
afterbitwise4 = cv2.erode(afterbitwise4,kernel_Abig)
afterbitwise4 = cv2.dilate(afterbitwise4,kernel_Abig1)

cv2.imshow("13_ThresholdCol3ofAnswers",afterbitwise4)
cv2.imwrite("dist/13_ThresholdCol3ofAnswers.jpg",afterbitwise4)

answersOfcol3XY = []
answersOfcol3 = []
for drawcirclie in range(102,551,32):
    print drawcirclie
    cv2.circle(afterbitwise4,(220,drawcirclie),6,(255,255,255),1)

cv2.imshow("14_ThresholdCol3ofAnswersDetectAnswersplusdrawImage",afterbitwise4)
cv2.imwrite("dist/14_ThresholdCol3ofAnswersDetectAnswersplusdrawImage.jpg",afterbitwise4)

img3,contourss3, hierarchys = cv2.findContours(afterbitwise4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss3:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    if int(radius) > 5 and int(radius) < 8 and col3rect[int(y),int(x)] < 215:
        print 'col3' ,  y
        cv2.circle(col3rect,(int(x),int(y)),3,(0,255,255),3)
        answersOfcol3XY.append([x,y])


cv2.imshow("15_Col3ofAnswersDetectAnswersplusdrawImage",col3rect)
cv2.imwrite("dist/15_Col3ofAnswersDetectAnswersplusdrawImage.jpg",col3rect)

previousrowYcol3 = 522
startptcol3 = 0
rowcol3 = 46
print "answersOfcol3XY" , answersOfcol3XY

for answer in xrange(len(answersOfcol3XY) ):
    if(answersOfcol3XY[answer][1] > 60 and answersOfcol3XY[answer][1] < 560 ):
        if(not(answersOfcol3XY[answer][1] > previousrowYcol3 - 4 and answersOfcol3XY[answer][1] < previousrowYcol3 + 4)):
            startptcol3 += 1
            rowcol3 -= 1
        if(answersOfcol3XY[answer][0] > 87 and answersOfcol3XY[answer][0] < 100 ):
            answersOfcol3.append([rowcol3 ,'A'])
        elif(answersOfcol3XY[answer][0] > 120 and answersOfcol3XY[answer][0] < 130 ):
            answersOfcol3.append([rowcol3 ,'B'])
        elif(answersOfcol3XY[answer][0] > 153 and answersOfcol3XY[answer][0] < 165 ):
            answersOfcol3.append([rowcol3 ,'C'])
        elif(answersOfcol3XY[answer][0] > 186 and answersOfcol3XY[answer][0] < 195 ):
            answersOfcol3.append([rowcol3 ,'D'])
        else:
            answersOfcol3.append([rowcol3 ,'Err'])
        previousrowYcol3 = answersOfcol3XY[answer][1]


#in col of ID
col4rect = cv2.resize(col4rect, (0,0), fx=2, fy=2)

col4rect = cv2.cvtColor(col4rect,cv2.COLOR_RGB2GRAY)
aftergauss5 = cv2.GaussianBlur(col4rect,(3,3),0)
afterthreshold5 = cv2.adaptiveThreshold(aftergauss5,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,75,10);
afterbitwise5 = cv2.bitwise_not( afterthreshold5)
kernel_Abigg = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
kernel_Abigg2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))

afterbitwise5 = cv2.erode(afterbitwise5,kernel_Abigg)
afterbitwise5 = cv2.dilate(afterbitwise5,kernel_Abigg2)

cv2.imshow("16_ThresholdColIDofAnswers",afterbitwise5)
cv2.imwrite("dist/16_ThresholdColIDofAnswers.jpg",afterbitwise5)

idNumList = []

img3,contourss4, hierarchys = cv2.findContours(afterbitwise5,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cont in contourss4:
    (x,y),radius = cv2.minEnclosingCircle(cont)
    print "radiusid" , x ,y
    if int(radius) > 5 and int(radius) < 9 and col4rect[int(y),int(x)] < 140:
        print x ,y
        cv2.circle(col4rect,(int(x),int(y)),3,(0,255,255),3)
        idNumList.append([x,y])


cv2.imshow("17_ThresholdColIDofAnswersDetectID",col4rect)
cv2.imwrite("dist/17_ThresholdColIDofAnswersDetectID.jpg",col4rect)

sortedidNumList = sorted(idNumList,key=lambda l:l[0])
numberofID = []
print "sortedidNumList", sortedidNumList
for num in xrange(len(sortedidNumList)):
    if(sortedidNumList[num][0] >84 and sortedidNumList[num][0] < 205 and  sortedidNumList[num][1] > 86 and sortedidNumList[num][1] < 438):
        if(sortedidNumList[num][1] >193 and sortedidNumList[num][1] < 205 ):
            numberofID.append(1)
        elif(sortedidNumList[num][1] >220 and sortedidNumList[num][1] < 228 ):
            numberofID.append(2)
        elif (sortedidNumList[num][1] >246 and sortedidNumList[num][1] < 258 ):
            numberofID.append(3)
        elif (sortedidNumList[num][1] >272 and sortedidNumList[num][1] < 280 ):
            numberofID.append(4)
        elif (sortedidNumList[num][1] >298 and sortedidNumList[num][1] < 308 ):
            numberofID.append(5)
        elif (sortedidNumList[num][1] >325 and sortedidNumList[num][1] < 334 ):
            numberofID.append(6)
        elif (sortedidNumList[num][1] >351 and sortedidNumList[num][1] < 359 ):
            numberofID.append(7)
        elif (sortedidNumList[num][1] >377 and sortedidNumList[num][1] < 388 ):
            numberofID.append(8)
        elif (sortedidNumList[num][1] >403 and sortedidNumList[num][1] < 411 ):
            numberofID.append(9)
        elif (sortedidNumList[num][1] >430 and sortedidNumList[num][1] < 438 ):
            numberofID.append(0)

def listtost(numList):
    s = map(str, numList)   # ['1','2','3']
    s = ''.join(s)          # '123'
    return s
print "ID" , listtost(numberofID)


#Answers
answers= []
answers = answersOfcol3 + answersOfcol2 + answersOfcol1
finalanswrswithouterr = []
for answer in xrange(len(answers)):
    if(not(answers[answer][1] == 'Err')):
        finalanswrswithouterr.append([answers[answer][0],answers[answer][1]])

print "finalanswrs" ,finalanswrswithouterr

#for printing on file
fo = open("output.txt", "wb")
fo.write(  "ID:\n")
fo.write(listtost(numberofID))
fo.write("\n")
fo.write("Answers:\n")
fo.write("\n")
for ans in finalanswrswithouterr:
    fo.write(str(ans[0]))
    fo.write(" : ")
    fo.write(str(ans[1]))
    fo.write("\n")
fo.close()






cv2.waitKey(0)
cv2.destroyAllWindows()