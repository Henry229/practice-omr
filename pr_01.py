import cv2
import numpy as np

image = cv2.imread("/Users/henry/Downloads/Math-Thinking-NSW.jpeg")
# image = cv2.imread("D:\\FinalOrm\\FinalOrm\\omr_hsc.jpg" ,0)
# image11 = cv2.imread("D:\\FinalOrm\\FinalOrm\\omr_has.jpg")

# correct_answers = ['B', 'B', 'B', 'A', 'A', 'D', 'D','C', 'C', 'B', 'C']

crop_img = image[157:975, 42:330]
answers = []

its = 0

for its in range(2):
    if its == 0:
       img1 = crop_img[0:818, 0:120]
    else:
       img1 = crop_img[0:818, 167:288]

    img1 = cv2.GaussianBlur(img1, (5,5), 0)
    img1 = cv2.Canny(img1, 100, 200)
    img1 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY,11,2)
    img1 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY,11,2)
    img1 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY,11,2)
    img1 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY,11,2)
    img1 = cv2.adaptiveThreshold(img1,255,cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY,11,2)
    img1 = cv2.GaussianBlur(img1, (5,5), 0)

    img = img1
    img = cv2.equalizeHist(img)

    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img1 = cv2.Canny(img1, 100, 200)
    img1 = cv2.Canny(img1, 100, 200)
    img1 = cv2.threshold(img1, 0, 255,  cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    img1 = cv2.GaussianBlur(img1, (5,5), 1)
    img1 = cv2.GaussianBlur(img1, (5,5), 1)

    circles = cv2.HoughCircles(img1, cv2.HOUGH_GRADIENT,1,10,param1=50, param2=30, minRadius=0, maxRadius=20) 

    circles = np.uint16(np.around(circles))
    k=0
    for i in circles[0,:]:
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        k=k+1
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for i in range(k):
        answers.append(circles[0][i][0] + circles[0][i][1] + circles[0][i][2])

sheet = len(answers)

final_answers = []
for i in range(0,200,4):
    j=i
    ind = -1
    index = ind 
    max = answers[j]
    for j in range(i+5):
        if max <= answers[j]:
            max = answers[j]
            ind = ind + 1
            index = ind
    if index == 0:
        final_answers.append('A')
    if index == 1:
        final_answers.append('B')
    if index == 2:
        final_answers.append('C')
    if index == 3:
        final_answers.append('D')
    if index > 3:
        final_answers.append('E')
    
mark = 0
itrr = len(final_answers)
for i in range(itrr):
    if final_answers[i] == correct_answers[i]:
        mark = mark + 1
print(final_answers)
print(mark)

font = cv2.FONT_HERSHEY_SIMPLEX

cv2.putText(image11, 'Marks: 22/50', (20, 450), font, 2, (0,0, 255), 3, cv2.LINE_AA)
cv2.imshow('marks', image11)
cv2.waitKey(0)
cv2.destroyAllWindows()