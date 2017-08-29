#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 20:37:19 2017

@author: wangxiujiang
"""

from sklearn.neural_network import MLPClassifier

import random

a1 = ['0000 - 0500 : Sleep', '0500 - 0700 : Essay', '0700 - 0900 : Essay', '0900 - 1200 : Classes', '1200 - 1400 : Event', '1400 - 1500 : Essay', '1500 - 1700 : Reading', '1700 - 2000 : Evening Execises', '2000 - 2200 : Essay', '2200 - 2300 : Essay', '2300 - 2359 : Sleep']

trainingdata = []
def preprocessing(a):
    dict1 = {}
    
    #0500-0900
    #1200-1700
    #2000-2300
    # other timings have fixed activities so not much point for the computer to learn anything
    
    for i in range (500,2300,50):
        if int(str(i)[-2:]) == 50:
            i = i -20
        if (i >= 900 and i < 1200) or (i >= 1700 and i < 2000):
            continue
        else:
            dict1[i] = "free"
    
    for i in range (500,2300,50):
        for j in range (len(a)):
            if int(str(i)[-2:]) == 50:
                i = i -20
            if (i >= 900 and i < 1200) or (i >= 1700 and i < 2000):
                continue
            elif i >= int(a[j][0:5]) and i < int(a[j][7:11]):
                    dict1[i] = a[j][14:]
            
    #print(dict1)
    
    #print(int(a[1][0:5]),int(a[1][7:11]),a[1][13:] )
    
    #neural network
    
    b = [v for v in dict1.values()]
    print(b)
    c =[]
    # convert names into num_labels (Essay = 1, Event = 2 Reading = 3, Assigned Reading = 4). For now, we will just use the name of the label, next time when variety of names is higher can group into various classes of activities using NLP or manual
    # c is the list of numbers for the labels
                                    
    for i in b:
        if i == 'Essay':
            c.append(1)
        elif i =='Event':
            c.append(2)
        elif i =='Reading':
            c.append(3)
        elif i =='Assigned Reading':
            c.append(4)
            
    return c

    trainingdata.append(c)

# X is the training set(m*n)--> m is the number of samples and n is the number of features ie len(c), y is the results set (m*1 vector)(where each value is 0 (no good plan) or 1 (good plan))
# for y values, I need user input for training. For now, I will just use fake data

# I will create a 30*n X training data and 30* 1 training data

X =[]
y =[]
for j in range(30):
    onedata =[]
    for i in range(24):
        onedata.append(random.randint(1,3))
    X.append(onedata)
    y.append(random.randint(0,1))

# this is the actual machine learning algorithm

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y) 

# use this to predict what is good or not good.
#print(X)
#print(preprocessing(a1))

good_or_no_good = clf.predict(preprocessing(a1)) [0]

#good_or_no_good is a number (0 and 1) that tells you whether the plan is more likely to be good for you or bad for you

chance_of_good = clf.predict_proba(preprocessing(a1)) [0][1]

#chance_of_good is a number between 0 and 1 that tells you how likely the thing is good to be good. You should fit this number back into the your code(not now of course)

# how we will use the machine learning code to improve the performance over time is that, 
#chances are that there are more than one possible arrangement of stuff. 
#ML can then rank all the possible arrangements and then pick the most likely one. This part we need to discuss tmr
