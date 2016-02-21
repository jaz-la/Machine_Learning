#from itertools import groupby
import collections
import math
Image_number = 5000
Test_image_num = 1000
Class_num = 10
height = 28
width = 28
smooth_factor = 1.0
correct=0.0

trainimage = open('trainingimages.txt', 'r')
trainlabel = open('traininglabels.txt', 'r')

def convert2int(symbol):
    if(symbol==' '):
        return 0
    if(symbol=='#'):
        return 1
    if(symbol=='+'):
        return 2

#################################################
#####read image
Imagedata = list(range(Image_number))
for j in range(Image_number):
    tmp = []
    for i in range(height):
        tmp.extend(list(trainimage.readline()[:-1]))
    Imagedata[j] = list(map(convert2int,tmp))

#################################################
####read label
# map label into list
init_label = trainlabel.read()
label_str = init_label.splitlines()
labels = list(map(int,label_str))

#################################################
#parameter
#find prior probabilty

counter=collections.Counter(labels)

prior_prob = list(range(Class_num))
number_idx = list(range(Class_num))

for i in range(10):
   prior_prob[i] = counter[i]/Image_number
   number_idx[i] = [k for k,x in enumerate(labels) if x == i]

##############################################


####find likelihood
feature_map = list(range(Class_num))
for number in range(Class_num):
    d = list(range(len(number_idx[number])))
    count =list(range(height*width))
    for pixel in range(height*width):
        for i,idx in enumerate(number_idx[number]):
            tmp = Imagedata[idx][pixel]
            d[i] = tmp
        count[pixel] = collections.Counter(d)
        count[pixel][0]=(count[pixel][0]+smooth_factor)/(len(number_idx[number])+smooth_factor)
        count[pixel][1]=(count[pixel][1]+smooth_factor)/(len(number_idx[number])+smooth_factor)
        count[pixel][2]=(count[pixel][2]+smooth_factor)/(len(number_idx[number])+smooth_factor)
    feature_map[number] = count

############################################################
#read test image and features
testImage = open('testimages.txt', 'r')

Imagetest = list(range(Test_image_num))
for j in range(Test_image_num):
    tmp = []
    for i in range(height):
        tmp.extend(list(testImage.readline()[:-1]))
    Imagetest[j] = list(map(convert2int,tmp))

pred_ret = list(range(Test_image_num))

for test_num in range(Test_image_num):
    predict_ret = list(range(Class_num))
    for class_num in range(Class_num):
        for feature_num in range(height*width):
            fi = Imagetest[test_num][feature_num]
            v = feature_map[class_num][feature_num][fi]
            if v != 0:
                predict_ret[class_num] += math.log(v,2.0)
        predict_ret[class_num] = prior_prob[class_num]+predict_ret[class_num]

    pred_ret[test_num] = predict_ret.index(max(predict_ret))

###############################################################
#Verify the accuracy

fin = open('testlabels.txt', 'r')
testlabels = []
for i in range(Test_image_num):
    testlabels.append(int(fin.readline()[0]))
fin.close()

for i in range(Test_image_num):
    if(pred_ret[i]==testlabels[i]):
        correct = correct+1.0
correct = correct/float(Test_image_num)

print "correction rate:",correct
