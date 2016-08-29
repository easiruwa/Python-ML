################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2015                        #
#                  Russell Glick '17 and Ben Sklar '18                         #
#             Machine Learning in Python Arff File Generator                   #
#                              arffgen.py                                      #
#   (Original, pre-edited addition created by Diane Paverman and Eric Murray   #
#                       arffGenerator.py - created Summer '12)                 #
#                                                                              #
#   This attachment program is called in the main project and is used to       #
#   create an arff file that contains Time Series Representation of the data   #
#   that could be passed into Orange.                                          #
#                                                                              #
#   Notices: There is no main in this program. Below comments have not been    #
#            edited. This program does not need to be changed for different    #
#            files.                                                            #
#                                                                              #
#                         DON'T TOUCH THIS PROGRAM                             #
################################################################################

import csv
import math
import numpy as np
from scipy import stats
from saxpy import SAX
import os
from biosppy.signals import ecg
from biosppy.signals import eda
from biosppy.signals import resp

def getDataType(name):
    print("NAME: " +name)
    firstUnderscore = False
    for i in range(len(name)):
        firstUnderscore = name[i] == '_'
        if(firstUnderscore):
            DataType = name[i+1:]
            return DataType
        
def readMarks(marks):
    # this function reads the marks file and returns a list of lists
    # each inner list represents one line in the marks file, so the
    # start, end, and condition values for one task
    marksFile = csv.reader(open(marks))
    rows = []
    for row in marksFile:
        rows.append(row)
    rows.pop(0)  # this removes the unwanted header from the file
    return rows

def boundaries(marks):
    # based on the numbers given in the marks file, this function returns the
    # integer version of the start, end, and condition values for 
    # the current task
    item = marks[0]
    start = int(item[0])
    end = int(item[1])
    condition = int(item[2])
    return start, end, condition    
            

def readData(name, datatype):
    file = csv.reader(open(name))
    rows1 = []
    for row in file:
        rows1.append(row)
        
    length = len(rows1) # this ends up being the number of scans in the data
    rows2 = []
    
    if datatype.upper() == 'FNIRS':
        print("name: " + name)
        # the fNIRS data doesn't actually start until the 42nd line
        # so we remove the unwanted lines here
        for i in range(2):
            rows1.pop(0)
        #there are also extra columns after the fNIRS data
        #so we remove those unwanted columns here
        print(length)
        for i in range(length - 2): # -2 
            rows2.append(rows1[i][0:53])
        return rows2
    elif datatype.upper() == 'EEG':
        rows1.pop(0) # get rid of first row of labels
        for i in range((length)-1):
            rows2.append(rows1[i][:])
        return rows2
    
    elif datatype.upper() == 'ECG' or datatype.upper() == 'EDA' or datatype.upper() == 'RESPIRATION':
        #for i in range(27): # remove extra rows from the top
        rows1.pop(0)
        for i in range(length-1):
            rows2.append(rows1[i][0]) 
        return rows2

    # elif datatype.upper() == 'EDA':
    #     for i in range(2):
    #         rows1.pop(0)
    #     for i in range(length - 2):
    #         rows2.append(rows1[i][0])
    #     return rows2


def makeNums(list, datatype):
    # this function converts the string values from the fNIRS data 
    # into decimal values with the original amount of decimal places (8)
    # (list is a list of 52 lists (one for each channel) of all of the data)
    if datatype.upper() == 'FNIRS' or datatype.upper() == 'EEG':
        for i in range(len(list)):
            for j in range(len(list[i])):
                num = list[i][j]
                if num[0] == "-":
                    num = round(float(num[1:]) * -1, 8)
                    list[i][j] = num
                else:
                    list[i][j] = round(float(num), 8)
        return list
    
    # elif datatype.upper() == 'EDA':
    #     for i in range (len(list)):
    #         num = list[i]
    #         if num == "":
    #             continue
    #         else:
    #             list[i] = round(float(num), 8)
    #     return list

    elif (datatype.upper() == 'ECG' or datatype.upper() == 'EDA' or datatype.upper() == 'RESPIRATION'):      
        for i in range(len(list)):
            num = list[i]
            list[i] = round(float(num), 8)
        return list

    # elif datatype.upper() == 'RESPIRATION':
    #     for i in range (len(list)):
    #         num = list[i]
    #         list[i] = round(float(num), 8)
    #     return list

def getTask(file, marks):
    # this function returns a list named task composed of 52 lists 
    # (one for each channel)
    # containing the data for the duration of the given task
    start, end, condition = boundaries(marks)
    task = file[start-1:end]
    return task, condition

def getSlope(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings.

    # vals is a list of one channel's values during the current task
    sumX = sumY = sumXsquared = sumXY = 0
    n = len(vals)
    for i in range(n):
        sumX += i
        sumY += vals[i]
        sumXsquared += i*i
        sumXY += i*vals[i]

    # the slope must be a string in order to be written to the output file
    slope = str((sumXY - (sumX * sumY)/n) / (sumXsquared - (sumX**2 / n)))
    output.write(slope + ', ')    

def getAverage(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # the average must be a string in order to be written to the output file
    average = str(sum(vals) / len(vals))
    output.write(average + ', ')
    
def getMax(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    # vals is a list of one channel's values during the current task

    # the maximum must be a string in order to be written to the output file
    maximum = str(max(vals))
    output.write(maximum + ', ')    

def getMin(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
    # vals is a list of one channel's values during the current task

    # the minimum must be a string in order to be written to the output file
    minimum = str(min(vals))
    output.write(minimum + ', ')

def getFWHM(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
    # vals is a list of one channel's values during the current task

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # check if the max value is negative
    if max(vals) < 0:
        halfMax = ((min(vals)-max(vals))/2) + max(vals)
    else:
        halfMax = ((max(vals)-min(vals))/2) + min(vals)

    i = 0
    # looking for the index of the first instance of the halfMax 
    # value (one the closest one to it)    
    while i <= len(vals)-2 and ((halfMax-vals[i]) * (vals[i+1]-halfMax)) < 0:
        i += 1

    # looking for the index of the last instance of the halfMax 
    # value (one the closest one to it)    
    j = len(vals)-1
    while j >= 1 and ((halfMax-vals[j]) * (vals[j-1]-halfMax)) < 0:
        j -= 1

    # calculate the point between the indexes at which the first instance 
    # most likely intersects the half max value
    m = vals[i+1] - vals[i]
    if m == 0:
        left = i
    else:
        left = (halfMax - vals[i] + m * i) / m
    
    # calculate the point between the indexes at which the last instance 
    # most likely intersects the half max value
    n = vals[j]-vals[j-1]
    if n == 0:
        right = j
    else:
        right = (halfMax - vals[j] + n * j) / n

    # the value must be a string in order to be written to the output file
    output.write(str(right - left) + ', ')

def getPLA(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
      
    #vals is a list of one channel's values during the current task

    vals = filter(lambda x:x !="", vals) # remove empty strings

    numSegs = 2  # the number of segments the task is divided into
    n = len(vals) / numSegs  # the number of values in each segment
    segment = []  # this will hold the values for the current segment
    m = 0  # this will keep track of what index you're at in the data
    slopeSum = 0  # this will accumulate the sum of the slopes in order 
                  # to later get the average

    for i in range(numSegs):
        for j in range(n):
            segment.append(vals[m]) # adds the values of the current segment 
                                    # to the list
            m += 1
        # calculate the line of best fit for the current segment
        mean = float(sum(range(len(segment)))) / len(segment)
        sum1 = 0
        for r in range(len(segment)):
            sum1 += (r - mean)**2
        stdev = math.sqrt((1.0 / len(segment)) * sum1) + 1 #DIVIDING BY ZERO HERE# standard deviation
        avg = sum(vals) / len(vals)
        sum2 = 0
        for k in range(len(segment)):
            sum2 += float(((k - mean) * (segment[k] - avg))) / (stdev**2)
        slope = (1.0 / (len(segment) - 0)) * sum2 #DIVIDING BY ZERO HERE
        output.write(str(slope)+', ')  # value must be a string in order 
                                       # to write to the output file
        slopeSum += slope
        segment = []  # clear out the list for the next segment

    avgSlope = slopeSum / numSegs
    output.write(str(avgSlope)) # value must be a string in order to write 
                                # to the output file
    output.write(', ')

def getStdev(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    stdev = np.std(vals)
    output.write(str(stdev) + ', ')


#Created by Mitchel Herman and Sindy Liu Summer 2016
def getVariance(task, index, output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    #vals is a list of one channel's values during the current task
    
    variance = np.var(vals)
    
    output.write(str(variance) + ', ') # value must be a string in order to write 
                                      # to the output file                           
                                      
#Created by Mitchel Herman and Sindy Liu Summer 2016
def getKurtosis(task, index, output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    #vals is a list of one channel's values during the current task
    
    kurtosis = stats.kurtosis(vals)
    
    output.write(str(kurtosis) + ', ') # value must be a string in order to write 
                                      # to the output file  
                                      
#Created by Mitchel Herman and Sindy Liu Summer 2016
def getZeroCrossings(task, index, output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    #vals is a list of one channel's values during the current task
    
    oldSign = np.sign(vals[0])
    crossings = 0
    for number in vals:
        currSign = np.sign(number)
        if(oldSign != currSign and currSign != 0):
            crossings += 1
        oldSign = currSign if currSign != 0 else oldSign
        
    output.write(str(crossings) + ', ') # value must be a string in order to write 
                                        # to the output file
                                        
#Created by Mitchel Herman and Sindy Liu Summer 2016
def getSkewness(task,index,output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    #vals is a list of one channel's values during the current task
    
    skewness = stats.skew(vals)
    output.write(str(skewness) + ', ')

#Created by Mitchel Herman and Sindy Liu Summer 2016
def getRMS(task, index, output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    #vals is a list of one channel's values during the current task
    
    squares = []
    for val in vals:
        squares.append(val*val)
    
    average = sum(squares) / len(squares)
    
    RMS = math.sqrt(average)
    output.write(str(RMS) + ', ') # value must be a string in order to write 
                                      # to the output file

def sax_rep(word,letter,ary):
    ary = np.asarray(ary)
    sax = SAX(word,letter)
    return sax.to_letter_rep(ary)

def getSAX(task,index,output, word, letter):

    # READ FROM TEXT FILE TO GET WORD AND LETTER
    #word =  # word length for each channel
    #letter = 5 # alphabet size, must be greater than 3, less than 20

    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    # vals is a list of one channel's values during the current task

    vals = filter(lambda x:x !="", vals) # remove empty strings

    sax = ""

    # sax becomes a series of letters generated from the SAX file
    sax += sax_rep(word,letter,vals)[0]
    newsax = ""
    for n in range(len(sax)):
        # converting the letters into characters
        newsax += (str((ord(str(sax[n]))-96)))

    # SAX output is a string with 4 numbers
    # output each number individually to the arff file
    # each individual number has its own SAX value (eg if newsax = '5314'
    #    SAX_1 = 5, SAX_2 = 3...)
    for x in range(word):
        output.write(newsax[x] + ',')

# Created by Eseosa Asiruwa Summer 2016
def getStdev(task,index,output):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    stdev = np.std(vals)
    output.write(str(stdev) + ', ')

# Created by Eseosa Asiruwa Summer 2016
def getHeartRate(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract heartrate using biosppy
    # vals is raw ECG data
    out = ecg.ecg(signal=signal, sampling_rate=samp_rate, show=False)

    # indexed number corresponds to the returned tuples from out
    # check biosppy files for more info
    out_heart_rate = out[6].tolist() # using numpy, convert ndarry into a list

    for x in out_heart_rate:
        output.write(out_heart_rate[x] +',')

# Created by Eseosa Asiruwa Summer 2016
def getHeartRateAvg(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract heartrate and rpeak features using biosppy
    # vals is raw ECG data
    out = ecg.ecg(signal=vals, sampling_rate=samp_rate, show=False)

    # indexed numbers correspond to the returned tuples from out
    # check biosppy files for more info
    out_heart_rate = out[3].tolist() # using numpy, convert ndarry into a list

    average = str(int(sum(out_heart_rate)) / len(out_heart_rate))
    output.write(average + ', ')

# Created by Eseosa Asiruwa Summer 2016
# def getRPeaksAvg(task,index,output,samp_rate):
#     vals = []
#     # making sure we are able to get values whether or not they are in a 
#         # two-dimensional array
#     for i in range(len(task)):
#         try:
#             vals.append(task[i][index])
#         except:
#             vals.append(task[i])

#     vals = filter(lambda x:x !="", vals) # remove empty strings
#     # extract heartrate feature using biosppy
#     # vals is raw ECG data
#     out = ecg.ecg(signal=vals, sampling_rate=samp_rate, show=False)

#     # indexed numbers correspond to the returned tuples from out
#     # check biosppy files for more info
#     out_r_peaks = out[2].tolist() # using numpy, convert ndarry into a list

#     rpeaks = []
#     for x in range(len(out_r_peaks)):
#         r_indicies = vals[out_r_peaks[x]]
#         rpeaks.append(r_indicies)

#     if (len(rpeaks)) == 0: # no pulse amplitudes found
#         output.write('0' + ', ')
#     else:
#         average = str(int(sum(rpeaks)) / len(rpeaks))
#         output.write(average + ', ')

# Created by Eseosa Asiruwa Summer 2016
def getSCRAvg(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    out = eda.eda(signal=vals, sampling_rate=samp_rate, show=False)

    # getting pulse amplitudes
    out_scr = out[4].tolist() # using numpy, convert ndarry into a list

    if (len(out_scr)) == 0: # no pulse amplitudes found
        output.write('0' + ', ')
    else:
        average = str(int(sum(out_scr)) / len(out_scr))
        output.write(average + ', ')

# Created by Eseosa Asiruwa Summer 2016
def getRespAvg(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract respiration features using biosppy
    # vals is raw resp data
    out = resp.resp(signal=vals, sampling_rate=samp_rate, show=False)       

    # getting instantaneous respiration rate
    out_resp = out[4].tolist() # using numpy, convert ndarry into a list

    if (len(out_resp)) == 0: # no respiration found
        output.write('0' + ', ')
    else:
        average = str(int(sum(out_resp)) / len(out_resp))
        output.write(average + ', ')

def getRespMin(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract respiration features using biosppy
    # vals is raw resp data
    out = resp.resp(signal=vals, sampling_rate=samp_rate, show=False)       

    # getting instantaneous respiration rate
    out_resp = out[4].tolist() # using numpy, convert ndarry into a list

    minimum = str(min(out_resp))
    output.write(minimum + ', ')

# Created by Eseosa Asiruwa Summer 2016
def getRespMax(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract respiration features using biosppy
    # vals is raw resp data
    out = resp.resp(signal=vals, sampling_rate=samp_rate, show=False)       

    # getting instantaneous respiration rate
    out_resp = out[4].tolist() # using numpy, convert ndarry into a list

    maximum = str(max(out_resp))
    output.write(maximum + ', ')  

def getFiltered_Max(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract eda features using biosppy
    # vals is raw eda data
    out = eda.eda(signal=vals, sampling_rate=samp_rate, show=False)       

    # getting filtered EDA signal
    out_eda_filtered = out[1].tolist() # using numpy, convert ndarry into a list

    maximum = str(max(out_eda_filtered))
    output.write(maximum + ', ')  

def getFiltered_Min(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract eda features using biosppy
    # vals is raw eda data
    out = eda.eda(signal=vals, sampling_rate=samp_rate, show=False)       

    # getting filtered EDA signal
    out_resp_filtered = out[1].tolist() # using numpy, convert ndarry into a list

    minimum = str(min(out_resp_filtered))
    output.write(minimum + ', ')  

def getUnfiltered_max(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
    
    # vals array is raw data
    vals = filter(lambda x:x !="", vals) # remove empty strings

    maximum = str(max(vals))
    output.write(maximum + ', ')

def getUnfiltered_min(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
    
    # vals array is raw data
    vals = filter(lambda x:x !="", vals) # remove empty strings

    minimum = str(min(vals))
    output.write(minimum + ', ')

def getRateChange_Min(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
    
    # vals array is raw data
    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract heartrate using biosppy
    # vals is raw ECG data
    out = ecg.ecg(signal=vals, sampling_rate=samp_rate, show=False)

    # indexed number corresponds to the returned tuples from out
    # check biosppy files for more info
    out_heart_rate = out[6].tolist() # using numpy, convert ndarry into a list

    # look through the formed heart rate list and find the changes in rate
    # create a new list with the rates of change
    # output the lowest rate of change
    hr_changes = []
    for i in range(len(out_heart_rate)):
        rate_change = out_heart_rate[i] - out_heart_rate[i-1]
        hr_changes.append(rate_change)

    minimum = str(min(hr_changes))
    output.write(minimum + ', ')

def getRateChange_Max(task,index,output,samp_rate):
    vals = []
    # making sure we are able to get values whether or not they are in a 
        # two-dimensional array
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])
    
    # vals array is raw data
    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract heartrate using biosppy
    # vals is raw ECG data
    out = ecg.ecg(signal=vals, sampling_rate=samp_rate, show=False)

    # indexed number corresponds to the returned tuples from out
    # check biosppy files for more info
    out_heart_rate = out[6].tolist() # using numpy, convert ndarry into a list

    # look through the formed heart rate list and find the changes in rate
    # create a new list with the rates of change
    # output the highest rate of change
    hr_changes = []
    for i in range(len(out_heart_rate)):
        rate_change = out_heart_rate[i] - out_heart_rate[i-1]
        hr_changes.append(rate_change)

    maximum = str(max(hr_changes))
    output.write(maximum + ', ')

def getHR_Std(task,index,output,samp_rate):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract heartrate using biosppy
    # vals is raw ECG data
    out = ecg.ecg(signal=vals, sampling_rate=samp_rate, show=False)

    # indexed number corresponds to the returned tuples from out
    # check biosppy files for more info
    out_heart_rate = out[6].tolist() # using numpy, convert ndarry into a list

    stdev = np.std(out_heart_rate)
    output.write(str(stdev) + ', ')

def getResp_std(task,index,output,samp_rate):
    vals = []
    for i in range(len(task)):
        try:
            vals.append(task[i][index])
        except:
            vals.append(task[i])

    vals = filter(lambda x:x !="", vals) # remove empty strings

    # extract respiration features using biosppy
    # vals is raw resp data
    out = resp.resp(signal=vals, sampling_rate=samp_rate, show=False)       

    # getting instantaneous respiration rate
    out_resp = out[4].tolist() # using numpy, convert ndarry into a list

    stdev = np.std(out_resp)
    output.write(str(stdev) + ', ')

def writeHeader(channels,output,conditions,relation,datatype, SAX, SAX_Word):
    if datatype.upper() == 'EEG':
        fileTypes = ['thetaslow', 'thetafast', 'thetatoal', 'alphaslow',
                     'alphafast', 'alphatotal', 'beta', 'gamma', 'sigma']
    elif datatype.upper() ==  'FNIRS':
        fileTypes = ['deoxy', 'oxy']
    elif datatype.upper() == 'ECG':
        fileTypes = ['ecg']
    elif datatype.upper() == 'EDA':
        fileTypes = ['eda']
    elif datatype.upper() == 'RESPIRATION':
        fileTypes = ['respiration']
    
    period = ['first_half', 'second_half', 'total']
    
    attributes = ['slope', 'average', 'max', 'min', 'full_width_at_half_max',
                  'PLA_1', 'PLA_2', 'PLA_Average'] 

    if(datatype.upper() == 'FNIRS'):
        attributes += ['variance', 'kurtosis', 'zero_crossings', 'skewness', 'RMS']
    elif datatype.upper() == 'ECG':
        attributes = ['heart_rate_avg', 'rate_change_min', 'rate_change_max', 'heart_rate_std']
    elif datatype.upper() == 'EDA':
        attributes = ['filtered_min', 'unfiltered_max', 'filtered_max', 'unfiltered_min']
    elif datatype.upper() == 'RESPIRATION':
        attributes = ['resp_avg', 'resp_min', 'resp_max', 'resp_std']

    if SAX:
        for i in range(SAX_Word):
            attributes.append("SAX_" + str(i))
               
    # write the relation and all of the attribute lines to the output file
    output.write('@RELATION ' + relation + '\r\n')
    for i in range(1,channels+1):
        for j in fileTypes:
            for k in attributes:
                for m in period:
                    output.write('@ATTRIBUTE ')
                    output.write('CHANNEL-'+ str(i) + '-'+ j)
                    output.write('-' + k + '-' + m +' NUMERIC' + '\r\n') 
                    
    output.write('@ATTRIBUTE condition ' + conditions + '\r\n')  
    output.write('@data \r\n')    

def writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter, sampling_rate):
    # this calls all of the functions on the given task for the first half, 
    # second half, and entirety
    # of the data from the given task
    half = len(task) / 2  # firstHalf will be smaller if len(task) is odd
    firstHalf = []
    # accumulate the list of the data for the first half
    for i in range(half):
        firstHalf.append(task[i])

    # accumulate the list of the data for the second half
    secondHalf = []
    for i in range(half,len(task)):
        secondHalf.append(task[i])
    
    # a list of all of the functions to be called on the data    
    functions = [getSlope, getAverage, getMax, getMin, getFWHM, getPLA]
    if(datatype.upper() ==  'FNIRS'):
        functions += [getVariance, getKurtosis, getZeroCrossings, getSkewness , getRMS]
    
    elif datatype.upper() == 'ECG':
        functions = [getHeartRateAvg, getRateChange_Min, getRateChange_Max, getHR_Std]

    elif datatype.upper() == 'EDA':
        functions = [getFiltered_Min, getUnfiltered_max, getFiltered_Max, getUnfiltered_min]

    elif datatype.upper() == 'RESPIRATION':
        functions = [getRespAvg, getRespMin, getRespMax, getResp_std]

    if SAX:
        functions += [getSAX]

    # calls all of the functions on all of the channels for the given task
    #for i in range(1, channels+1):
    for i in range(channels):
        for j in functions:
            if j == getSAX:
                j(firstHalf,i,output, SAX_Word, SAX_Letter)
                j(secondHalf,i,output, SAX_Word, SAX_Letter)
                j(task,i,output, SAX_Word, SAX_Letter)

            elif (j == getHeartRateAvg or j == getRateChange_Min or j == getRateChange_Max
                or j == getRespAvg or j == getRespMin or j == getRespMax
                or j == getFiltered_Min or j == getUnfiltered_max or j == getFiltered_Max 
                or j == getUnfiltered_min or j == getHR_Std or j == getResp_std):
                j(firstHalf,i,output, sampling_rate)
                j(secondHalf,i,output, sampling_rate)
                j(task,i,output, sampling_rate)

            else:
                j(firstHalf,i,output)
                j(secondHalf,i,output)
                j(task,i,output)
                
def arff_generate(inp,conds,subs,channels,cl, SAX, SAX_Word, SAX_Letter, sampling_rate):
    # cl is just the list of conditions that you can input in the main
    relation = 'trust'  # probably going to be passed in in the main file
    conditions = '{'
    datatype = getDataType(inp)
    print("HERES THE DATA TYPE IN ARFFGEN:" + datatype)
    #for i in range(conds-1):
    for i in range(len(cl)-1):
        conditions += (cl[i]+', ')
    conditions += (cl[len(cl)-1]+'}')

    print ("conditions")
    print (conditions)
    # this massive loop generates an .arff file for every subject and puts 
    # them in the output folder indicated at the top of this program
    for i in range(1,subs+1):
        marks = inp + '_Marks.csv'
        output = open(inp+'_Arff.arff', 'w') 
        if datatype.upper() == 'FNIRS':
            deoxy = inp + '_Deoxy.csv'
            oxy = inp + '_Oxy.csv'

            # read in the values from the Excel files
            marks = readMarks(marks)
            deoxy = readData(deoxy, datatype)
            oxy = readData(oxy, datatype)

            # convert the values from the Excel files from strings to integers
            deoxy = makeNums(deoxy,datatype)
            oxy = makeNums(oxy,datatype)

            # writes the header of the .arff file
            writeHeader(channels,output,conditions,relation,datatype, SAX, SAX_Word)

            # this loop is responsible for going through the deoxy, oxy, and total
            # data files, running all of the necessary func tions, and writing all
            # of the necessary output to the output file for each task indicated by
            # each line of the marks file
            for i in range(len(marks)):
                task, condition = getTask(deoxy, marks)
                writeTasks(task,channels,output,datatype,SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(oxy, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                output.write(str(condition))
                output.write('\r\n\r\n')  #each task is separated by 2 new lines
                marks.pop(0)  #proceed to the next task  

            output.close()

        elif datatype.upper() == 'EDA':
            eda = inp + '_All_Data.csv'

            marks = readMarks(marks)

            eda = readData(eda,datatype)

            eda = makeNums(eda,datatype)

            writeHeader(channels,output,conditions,relation,datatype, SAX, SAX_Word)

            for i in range(len(marks)):
                task, condition = getTask(eda, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                output.write(str(condition))
                output.write('\r\n\r\n')  #each task is separated by 2 new lines
                marks.pop(0)  #proceed to the next task 

            output.close()

        elif datatype.upper() == 'RESPIRATION':
            respiration = inp + '_All_Data.csv'
            marks = readMarks(marks)

            respiration = readData(respiration,datatype)

            respiration = makeNums(respiration,datatype)
            writeHeader(channels,output,conditions,relation,datatype, SAX, SAX_Word)
            for i in range(len(marks)):
                task, condition = getTask(respiration, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                output.write(str(condition))
                output.write('\r\n\r\n')  #each task is separated by 2 new lines
                marks.pop(0)  #proceed to the next task 

            output.close()

        elif datatype.upper() == 'ECG':
            ecg = inp + '_All_Data.csv'

            marks = readMarks(marks)

            ecg = readData(ecg,datatype)

            ecg = makeNums(ecg,datatype)

            writeHeader(channels,output,conditions,relation,datatype, SAX, SAX_Word)

            for i in range(len(marks)):
                task, condition = getTask(ecg, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                output.write(str(condition))
                output.write('\r\n\r\n')  #each task is separated by 2 new lines
                marks.pop(0)  #proceed to the next task  

            output.close()

        elif datatype.upper() == 'EEG':
            thetaslow = inp + '_ThetaSlow.csv'
            thetafast = inp + '_ThetaFast.csv'
            thetatotal = inp + '_ThetaTotal.csv'
            alphaslow = inp + '_AlphaSlow.csv'
            alphafast = inp + '_AlphaFast.csv'
            alphatotal = inp + '_AlphaTotal.csv'
            beta = inp + '_Beta.csv'
            gamma = inp + '_Gamma.csv'
            sigma = inp + '_Sigma.csv'

            # read in values from the excel files
            marks = readMarks(marks)
            thetaslow = readData(thetaslow, datatype)
            thetafast = readData(thetafast, datatype)
            thetatotal = readData(thetatotal, datatype)
            alphaslow = readData(alphaslow, datatype)
            alphafast = readData(alphafast, datatype)
            alphatotal = readData(alphatotal, datatype)
            beta = readData(beta, datatype)
            gamma = readData(gamma, datatype)
            sigma = readData(sigma, datatype)

            # convert values from the excel files from strings to integers
            thetaslow = makeNums(thetaslow,datatype)
            thetafast = makeNums(thetafast,datatype)
            thetatotal = makeNums(thetatotal,datatype)
            alphaslow = makeNums(alphaslow,datatype)
            alphafast = makeNums(alphafast,datatype)
            alphatotal = makeNums(alphatotal,datatype)
            beta = makeNums(beta,datatype)
            gamma = makeNums(gamma,datatype)
            sigma = makeNums(sigma,datatype)
            
            # writes the header of the .arff file
            writeHeader(channels,output,conditions,relation,datatype, SAX, SAX_Word)

            for i in range(len(marks)):
                task, condition = getTask(thetaslow, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(thetafast, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(thetatotal, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(alphaslow, marks)
                writeTasks(task,channels,output,datatype,SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(alphafast, marks)
                writeTasks(task,channels,output,datatype,SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(alphatotal, marks)
                writeTasks(task,channels,output,datatype,SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(beta, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(gamma, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                task, condition = getTask(sigma, marks)
                writeTasks(task,channels,output,datatype, SAX, SAX_Word, SAX_Letter,
                    sampling_rate)
                output.write(str(condition))
                output.write('\r\n\r\n')  #each task is separated by 2 new lines
                marks.pop(0)  #proceed to the next task   

            # Remove all of EEG sub-files
            os.remove(inp + '_ThetaSlow.csv')
            os.remove(inp + '_ThetaFast.csv')
            os.remove(inp + '_ThetaTotal.csv')
            os.remove(inp + '_AlphaSlow.csv')
            os.remove(inp + '_AlphaFast.csv')
            os.remove(inp + '_AlphaTotal.csv')
            os.remove(inp + '_Beta.csv')
            os.remove(inp + '_Gamma.csv')
            os.remove(inp + '_Sigma.csv')  
              
            output.close()
