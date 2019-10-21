# -*- coding: utf-8 -*-
"""LetterClassifications.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l6Uxy-eWoNYJKZ1DUdou3GTQaT2cI2yb
"""

pip install scikit-tda

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from numpy import genfromtxt
from ripser import ripser,lower_star_img
from persim import plot_diagrams

from google.colab import files
uploaded= files.upload()

letters = genfromtxt('letters.csv', delimiter =',')
#the main block: run 6 scans for each of the 26 letters, store results in a dictionary.
i=0
i_to_result = dict()
while i<=25:
    letter_one_line = letters[i,:]
#initialize matrix of size 10x10 with all values 100
    letter= np.full((10,10),100)
   #test 1 probing upper left
    for k in range(1,100):
        if letter_one_line[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= max((k-1)%10, int((k-1)/10))
    PUscan = lower_star_img(letter)
    #test 2 left to right
    for j in range(1,100):
        if letter_one_line[j]==1.0:
            row=int((j-1)/10)
            column= (j-1)%10
            letter[row,column]= j%10
    LRscan = lower_star_img(letter)
    #test 3 right to left
    for k in range(1,100):
        if letter_one_line[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= 10 - (k-1)%10
    RLscan = lower_star_img(letter)
    #test 4 probing from bottom right
    for k in range(1,100):
        if letter_one_line[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= max(9-(k-1)%10,9-int((k-1)/10))  
    PLBscan = lower_star_img(letter)
    #test 5 probing from upper right to lower left 
    for k in range(1,100):       
        if letter_one_line[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= max(9-(k-1)%10,int((k-1)/10))  
    PURscan = lower_star_img(letter) 
    #test 6
    letter_ones_line = letters[i,1:]
    newletter = letter_ones_line.reshape(10,10)
    coordinates = np.argwhere(newletter == 1)
    dgms = ripser(coordinates)['dgms']
    h1_test = dgms[1]
    
    i_to_result[i] = (PUscan, LRscan, RLscan, PLBscan, PURscan, h1_test)
    i+=1

#change all infinity in life-death pair to 100.    
l=0
while l <=25:
    for j in range(6):
        len_j = len(i_to_result[l][j])
        for k in range(len_j):
            if str(i_to_result[l][j][k][1])=='inf':
                i_to_result[l][j][k][1]=100
    l+=1
#calculate feature vector for each letter, store them in a matrix. 
#every feature vector has 5 components, each component stands for the sum of "lifespan" of the life-death pairs in one scan.
l=0
vec_mtx = np.zeros((26,6))
while l < 26:
    for j in range(6):
        len_j = len(i_to_result[l][j])
        sum_j = 0
        for k in range(len_j):
            sum_j = sum_j+ (i_to_result[l][j][k][1]-i_to_result[l][j][k][0])
            vec_mtx[l][j] = sum_j
    l+=1
print('feature matrix:\n',vec_mtx,'\n')

#calculate the pairwise distance between each two letter, store them in a list.
all_dis = []
for q in range(26):
    for p in range(q):
            dis = np.linalg.norm(vec_mtx[q]-vec_mtx[p])
            all_dis.append((dis,p,q))

#sort all the distance from low to high, find the minimum distance, also find which letter pair has the minimum distance.             
def getkey(item):
    return item[0]

sorted_dis = sorted(all_dis, key=getkey)
print('how many items in this sorted distance list:',len(sorted_dis),'\n','sorted distance:',sorted_dis,'\n')

print('min distance is between',sorted_dis[0][1],'th letter and',sorted_dis[0][2],'th letter. min distance is',sorted_dis[0][0],'\n')

Letters= pd.read_csv("letters.csv")
Letters[9:10]

#convert new test input list of 01010101... into feature vector.
def get_feature_vec(test): # 'test' stands for the 01010101... input.
    #run all the scans, get the life-death pairs.
    letter= np.full((10,10),100)
   #test 1 probing upper left
    for k in range(1,100):
        if test[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= max((k-1)%10, int((k-1)/10))
    PUscan = lower_star_img(letter)
    #test 2 left to right
    for j in range(1,100):
        if test[j]==1.0:
            row=int((j-1)/10)
            column= (j-1)%10
            letter[row,column]= j%10
    LRscan = lower_star_img(letter)
    #test 3 right to left
    for k in range(1,100):
        if test[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= 10 - (k-1)%10
    RLscan = lower_star_img(letter)
    #test 4 probing from bottom right
    for k in range(1,100):
        if test[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= max(9-(k-1)%10,9-int((k-1)/10))  
    PLBscan = lower_star_img(letter)
    #test 5 probing from upper right to lower left 
    for k in range(1,100):       
        if test[k]==1.0:
            row=int((k-1)/10)
            column= (k-1)%10
            letter[row,column]= max(9-(k-1)%10,int((k-1)/10))  
    PURscan = lower_star_img(letter) 
    #test 6
    newletter = test[1:].reshape(10,10)
    coordinates = np.argwhere(newletter == 1)
    dgms = ripser(coordinates)['dgms']
    h1_test = dgms[1]
    test_result = (PUscan, LRscan, RLscan, PLBscan, PURscan, h1_test)
    #change all infini to 100
    for j in range(6):
        len_j = len(test_result[j])
        for k in range(len_j):
            if str(test_result[j][k][1])=='inf':
                test_result[j][k][1]=100
    #get the feature vector
    test_feature = np.zeros(6)
    for j in range(6):
        len_j = len(test_result[j])
        sum_j = 0
        for k in range(len_j):
            sum_j = sum_j+ (test_result[j][k][1]-test_result[j][k][0])
            test_feature[j] = sum_j
            
    return test_feature

#make up a test list. I wrote the letter S (the 18th letter) in 10X10 grid, and recored the coordinates in one_list.
#New_C = letters[4]
#New_C = [11,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
New_C = [11,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
#New_C = [9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#New_C = [9,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
New_C = np.asarray(New_C)
plt.imshow(New_C[1:].reshape(10,10))
print(New_C)
feature_vect = get_feature_vec(New_C)


print('feature vect of input list is:',feature_vect)
#print('standard feature vect of c is:', vec_mtx[3])

#compare the newly obtained test feature vector, to each of the feature vector stored in matrix.
test_dis = []
for i in range(len(vec_mtx)):
    # compare feature_vect with each of the vect in vec_mtx, see which distance=norm(feature_vect - vect) is smalletst.
    d = np.linalg.norm(feature_vect - vec_mtx[i])
    test_dis.append((d,i))
    
#then find the which vector has the smallest distance with input test vector, choose it as our best fitted letter.
sorted_result = sorted(test_dis,key=getkey)
print('the best fitted letter is:',sorted_result[0][1],'th letter','\n','the closest distance is:',sorted_result[0][0],'\n')
     #'other option:',sorted_result[1],sorted_result[2],sorted_result[3],'\n')

#print('full resulting distance:','\n',sorted_result)

k = letters[4]
plt.imshow(k[1:].reshape(10,10))
vec_mtx[4]

