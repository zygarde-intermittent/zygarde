import csv
import matplotlib.pyplot as plt
import numpy as np
from general_CEE import persistentCEEgen, getKWdistance, binary_thresholding, countPlus, countMinus, calculateProb, genPlot, getRandomKW, getEta

def readData(filename):
    datas = []
    times = []
    
    with open('solar_data.csv') as csvFile:
        readCSV = csv.reader(csvFile, delimiter=',')
        i = 0
        for row in readCSV:
            if(i!=0):
                datas.append(float(row[1]))
                times.append(int(row[0]))
            i = i + 1
    return datas, times


E_threshold = 900 # this the threshold value of E. Here the unit is in mJ. It can be anything as needed. Voltage can also be used here.
size = 20
datas, times = readData('data.csv')
datas_binary = binary_thresholding(datas, E_threshold)
plus, totalP = countPlus(datas_binary, size+5)
minus, totalM = countMinus(datas_binary, size+5)
probPlus = calculateProb(plus, totalP, size)
probMinus = calculateProb(minus, totalM, size, minus_sign=1)
mergeArray = genPlot(probPlus, probMinus, size, file_write=0)

persistentArray = persistentCEEgen(size)
dc = getKWdistance(persistentArray.flatten(), mergeArray.flatten())

event_count = np.count_nonzero(np.asarray(solar_binary))
dr = getRandomKW(size, len(datas_binary), event_count)
print(getEta(dc, dr))
