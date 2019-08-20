import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
import random

def persistentCEEgen(size):
    probPlus = []
    probMinus = []
    for i in range(0, size):
        probPlus.append(1)
        probMinus.append(0)
    probMinusR = probMinus[::-1]
    mergedList = [*probMinusR, 0, *probPlus]
    mergeArray = np.asarray(mergedList)
    t = np.arange((size*-1), size+1, 1)
    return np.reshape(mergeArray, [-1,1])

def getKWdistance(array1, array2):
    print(len(array1), len(array2))
    if(len(array1) != len(array2)):
        print("inconsistent array size")
        return 
    dist = sc.wasserstein_distance(array1, array2)
    print(dist)
    return dist

def binary_thresholding(dataArray, threshold):
    binary = []
    for st in dataArray:
        if st < threshold:
            binary.append(0)
        else:
            binary.append(1)
    return binary

def countPlus(binary, size):
    plus = []
    totalP = []
    for n in range(1, size):
        pl = 0
        mn = 0
        ttl = 0
        for i in range(n, len(binary)-1):
            flag = 1
            for j in range(1, n):
                if(binary[i-j] == 0):
                    flag = 0
            if (flag == 1):
                if(binary[i] == 1):
                    pl = pl+1
                ttl = ttl + 1
        plus.append(pl)
        totalP.append(ttl)
    return plus, totalP

def countMinus(binary, size):
    minus = []
    totalM = []
    for n in range(1, size):
        mn = 0
        ttl = 0
        for i in range(n, len(binary)-1):
            flag = 1
            for j in range(1, n):
                if(binary[i-j] == 1):
                    flag = 0
            if (flag == 1):
                if(binary[i] == 1):
                    mn = mn+1
                ttl = ttl + 1
        minus.append(mn)
        totalM.append(ttl)
    return minus, totalM

def calculateProb(arr, total_arr, size, minus_sign=0):
    probArray = []
    for i in range(minus_sign, size+minus_sign):
        if total_arr[i] != 0:
            temp = (arr[i]/total_arr[i])
            probArray.append(temp)
        else:
            probArray.append(0)
    return probArray

def genPlot(probPlus, probMinus, size, file_write=0, filename = None):
    if(len(probPlus) != len(probMinus)):
        print("array size inconsistency")
        return 0
    probMinusR = probMinus[::-1]
    zeroPoint = (probMinus[0]+probPlus[0])/2
    mergedList = [*probMinusR, zeroPoint, *probPlus]
    t = np.arange((size*-1), (size+1), 1)
    mergeArray = np.asarray(mergedList)
    t = np.reshape(t, [-1,1])
    mergeArray = np.reshape(mergeArray, [-1,1])
    plt.plot(t, mergeArray)
    if file_write == 1:
        outS = np.concatenate((t, mergeArray), axis=1)
        print(outS.shape)
        np.savetxt(filename, outS, delimiter=",")
    return mergeArray

def randomCEEgen(size, event_count):
    randomList = [0] * size
    temp = random.sample(range(0, size-1), event_count)
    for x in temp:
        randomList[x] = 1
    np.count_nonzero(np.asarray(randomList)) 
    return randomList

def getRandomKW(size, arr_length, event_count):
    randomList = randomCEEgen(arr_length, event_count)
    plus, totalP = countPlus(randomList, size+5)
    minus, totalM = countMinus(randomList, size+5)
    probPlus = calculateProb(plus, totalP, size)
    probMinus = calculateProb(minus, totalM, size, minus_sign=1)
    mergeArray = genPlot(probPlus, probMinus, size, file_write=0)
    persistentArray = persistentCEEgen(size)
    dist = getKWdistance(persistentArray.flatten(), mergeArray.flatten())
    return dist

def getEta(dc, dr):
    return ((dr-dc)/dr)
