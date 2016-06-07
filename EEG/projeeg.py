################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2016                        #
#                 Eseosa Asiruwa '18 and Matt Goon '18                         #
#                                                                              #
#                                                                              #
################################################################################

import csv

#======================OPENING AND WRITING CSV FILES============================

def open_csv(name):
    sups = []
    with open(name,'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            sups.append(row)
    return sups

def write_csv(name,data):
    with open(name,'wb') as wf:
        a = csv.writer(wf,delimiter=',') 
        for i in range(len(data)):
            a.writerow(data[i])

#=============================FORMATTING========================================

# formatting-getting rid of the empty spaces
def first_row_format(lst,char):
    while len(lst) != 2:
        lst.remove(char)
    return lst

def data_format(lst,chans):
    for i in range(len(lst)-2):
        for j in range(chans*2):
            lst[i+2][j] = float(lst[i+2][j])
    return lst

def cond_format(lst):
    empt = lst[0][0]
    for i in range(len(lst)):
        while lst[i].count(empt) != 0:
            lst[i].remove(empt)
    for i in range(len(lst)-1):
        for j in range(len(lst[i+1])-2):
            lst[i+1][j+2] = int(lst[i+1][j+2])
    return lst

