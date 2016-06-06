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
    
def readfNIRS(name):
    # this function makes a list of lists called rows2 of all of the fNIRS data
    # each inner list is one row in the fNIRS data (so all of the 
    # channels' data from one scan)
    file = csv.reader(open(name))
    rows1 = []
    for row in file:
        rows1.append(row)
        
        # the fNIRS data doesn't actually start until the 4th line
        # so we remove the unwanted lines here
    for i in range(2):
        rows1.pop(0)
        
    length = len(rows1) # this ends up being the number of scans in the data
    rows2 = []
    # there are also extra columns after the fNIRS data
    # so we remove those unwanted columns here
    for i in range(length):
        rows2.append(rows1[i][0:53])
    return rows2

def makeNums(list):
    # this function converts the string values from the fNIRS data 
    # into decimal values with the original amount of decimal places (8)
    # (list is a list of 52 lists (one for each channel) of all of the data)
    for i in range(len(list)):
        for j in range(len(list[i])):
            num = list[i][j]
            if num[0] == "-":
                num = round(float(num[1:]) * -1, 8)
                list[i][j] = num
            else:
                list[i][j] = round(float(num), 8)
    return list

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
        vals.append(task[i][index])
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
        vals.append(task[i][index])
    # vals is a list of one channel's values during the current task

    # the average must be a string in order to be written to the output file
    average = str(sum(vals) / len(vals))
    output.write(average + ', ')
    
def getMax(task,index,output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    # vals is a list of one channel's values during the current task

    # the maximum must be a string in order to be written to the output file
    maximum = str(max(vals))
    output.write(maximum + ', ')    

def getMin(task,index,output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    # vals is a list of one channel's values during the current task

    # the minimum must be a string in order to be written to the output file
    minimum = str(min(vals))
    output.write(minimum + ', ')

def getFWHM(task,index,output):
    vals = []
    for i in range(len(task)):
        vals.append(task[i][index])
    # vals is a list of one channel's values during the current task

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
        vals.append(task[i][index])
    #vals is a list of one channel's values during the current task

    numSegs = 5  # the number of segments the task is divided into
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
        stdev = math.sqrt((1.0 / len(segment)) * sum1)  # standard deviation
        avg = sum(vals) / len(vals)
        sum2 = 0
        for k in range(len(segment)):
            sum2 += float(((k - mean) * (segment[k] - avg))) / (stdev**2)
        slope = (1.0 / (len(segment) - 1)) * sum2
        output.write(str(slope)+', ')  # value must be a string in order 
                                       # to write to the output file
        slopeSum += slope
        segment = []  # clear out the list for the next segment

    avgSlope = slopeSum / numSegs
    output.write(str(avgSlope)) # value must be a string in order to write 
                                # to the output file
    output.write(', ')

def writeHeader(channels,output,conditions,relation):
    fileTypes = ['deoxy', 'oxy']
    period = ['first_half', 'second_half', 'total'] 
    attributes = ['slope', 'average', 'max', 'min', 'full_width_at_half_max',
                  'PLA_1', 'PLA_2', 'PLA_3', 'PLA_4', 'PLA_5', 'PLA_Average']
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

def writeTasks(task,channels,output):
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
    functions = [getAverage, getMax, getMin, getSlope, getFWHM, getPLA]

    # calls all of the functions on all of the channels for the given task
    #for i in range(1, channels+1):
    for i in range(channels):
        for j in functions:
            j(firstHalf,i,output)
            j(secondHalf,i,output)
            j(task,i,output)

def arff_generate(inp,conds,subs,channels,cl):
    # cl is just the list of conditions that you can input in the main
    relation = 'trust'  # probably going to be passed in in the main file
    conditions = '{'
    #for i in range(conds-1):
    for i in range(len(cl)-1):
        conditions += (cl[i]+', ')
    conditions += (cl[len(cl)-1]+'}')
    # this massive loop generates an .arff file for every subject and puts 
    # them in the output folder indicated at the top of this program
    for i in range(1,subs+1):
        deoxy = inp + '_Deoxy.csv'
        oxy = inp + '_Oxy.csv'
        marks = inp + '_Marks.csv'
        output = open(inp+'_Arff.arff', 'w') 
        
        # read in the values from the Excel files
        marks = readMarks(marks)
        deoxy = readfNIRS(deoxy)
        oxy = readfNIRS(oxy)

        # convert the values from the Excel files from strings to integers
        deoxy = makeNums(deoxy)
        oxy = makeNums(oxy)

        # writes the header of the .arff file
        writeHeader(channels,output,conditions,relation)

        # this loop is responsible for going through the deoxy, oxy, and total
        # data files, running all of the necessary functions, and writing all
        # of the necessary output to the output file for each task indicated by
        # each line of the marks file
        for i in range(len(marks)):
            task, condition = getTask(deoxy, marks)
            writeTasks(task,channels,output)
            task, condition = getTask(oxy, marks)
            writeTasks(task,channels,output)
            output.write(str(condition))
            output.write('\r\n\r\n')  #each task is separated by 2 new lines
            marks.pop(0)  #proceed to the next task            
            
        output.close()
