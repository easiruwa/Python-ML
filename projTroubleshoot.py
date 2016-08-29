################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2016                        #
#                                                                              #
#                 Machine Learning in Python Main Project                      #
#                               proj.py                                        #
#                                                                              #
#   This Program will allow the user to run Symbolic Aggregate Approximation   #
#   and other miscellaneous Machine Learning techniques (see the attached      #
#   Diane Paverman/Eric Murray and Orange files) on an inputted set of data    #
#   and condition files. The names of these files, the choice to use ROI or    #
#   zscore, the Conditions being tested,lengths for SAX, and a couple of       #
#   parameters for Orange can be changed below in the main function,           #
#   highlighted by comments in capital letters in the section USER INPUTS.     #
#   Enjoy.                                                                     #
#                                                                              #
#   Credits: http://www.cs.ucr.edu/~eamonn/SAX.htm and                         #
#            https://github.com/nphoff/saxpy/blob/master/saxpy.py for SAX      #
#            instruction and the imported SAX class                            #
#                                                                              #
#            Diane Paverman and Eric Murray (Hamilton Summer Research 2012)    #
#            for their arff file generator                                     #
#                                                                              #
#            Orange (http://orange.biolab.si/) for their built in Machine      #
#            Learning algorithms                                               #
#                                                                              #
#            Mykhailo Antoniv (Hamilton College '17) and Eric Collins          #
#            (Hamilton College '17) for the comment format used in these       #
#            programs                                                          #
#                                                                              #
################################################################################

# from __future__ import print_function
import numpy as np
import csv
import os
from arffgen import arff_generate
from Orange_ML import orange
from Orange_ML_two import orange_two
from scipy import stats
import sys
import re
from arffconvertertotab import convert

# For accessing the data on the server
from zipfile import ZipFile
from urllib import urlopen
from StringIO import StringIO


#Dictionary stores the len of the attributes for each sensor (divided by the num chans)
arffLine = {}


# For accessing the data on the server (EDITED OUT)

#======================OPENING AND WRITING CSV FILES============================
def open_url(base_url, name):
    full_url = base_url+name+'.zip'

    print full_url
    
    zip_request = urlopen(full_url)
    zip_file = ZipFile(StringIO(zip_request.read()))
    data = StringIO(zip_file.read(name+'.csv'))
    csv_file = csv.reader(data)
    
    csv_out=[]
    for line in csv_file:
        csv_out.append(line)
    return csv_out

#Helper function used to open csv files
def open_csv(name):
    sups = []
    i = 0
    with open(name,'rU') as f:
        #reader = csv.reader(f, dialect = csv.excel_tab)
        reader = csv.reader(f)
        for row in reader:
            sups.append(row)
    return sups

#Helper function used to write csv files
def write_csv(name,data):
    with open(name,'wb') as wf:
        a = csv.writer(wf,delimiter=',')
        for i in range(len(data)):
            a.writerow(data[i])

#=========================SEPARATING DATA FOR ARFFGEN===========================

#for fNIRS and EEG, the All_Data files need to be seperated for use in the
#ArffGenerator. fNIRS gets split into oxy and deoxy, and EEG gets split up
#into each of the EEG forms.
#If you want to add more EEG data types in the future, add them to this function
#and change arffgen as well as arffline to correspond
def write_sep_data(data,chans,name,datatype):
    if(datatype.upper() == "FNIRS"):
        oxy = []
        deoxy = []
        for i in range(len(data)):
            oxy_row = []
            deoxy_row = []
            for j in range(chans):
                oxy_row.append(data[i][j])
                deoxy_row.append(data[i][j+chans])
            oxy.append(oxy_row)
            deoxy.append(deoxy_row)

        write_csv(name+'_Oxy.csv',oxy)
        write_csv(name+'_Deoxy.csv',deoxy)

    elif(datatype.upper() == "EEG"):
    # Create seperate arrays for each form of data (9 in total)
        theta_slow = []
        theta_fast = []
        theta_total = []
        alpha_slow = []
        alpha_fast = []
        alpha_total =[]
        beta = []
        gamma = []
        sigma = []
        for i in range(len(data)):
            tslow_row = []
            tfast_row = []
            ttotal_row = []
            afast_row = []
            aslow_row = []
            atotal_row =[]
            beta_row = []
            gamma_row = []
            sigma_row = []
            for j in range(chans):
                for k in range(10):
                    if k == 0 and j == 0:
                        # Add timestamps (epochs) to each data file
                        tslow_row.append(data[i][k])
                        tfast_row.append(data[i][k])
                        ttotal_row.append(data[i][k])
                        atotal_row.append(data[i][k])
                        beta_row.append(data[i][k])
                        gamma_row.append(data[i][k])
                        sigma_row.append(data[i][k])
                        afast_row.append(data[i][k])
                        aslow_row.append(data[i][k])
                    # Add corresponding data to each file, row by row
                    elif k == 1:
                        tslow_row.append(data[i][(9 * j) + k])
                    elif k == 2:
                        tfast_row.append(data[i][(9 * j) + k])
                    elif k == 3:
                        ttotal_row.append(data[i][(9 * j) + k])
                    elif k == 4:
                        aslow_row.append(data[i][(9 * j) + k])
                    elif k == 5:
                        afast_row.append(data[i][(9 * j) + k])
                    elif k == 6:
                        atotal_row.append(data[i][(9 * j) + k])
                    elif k == 7:
                        beta_row.append(data[i][(9 * j) + k])
                    elif k == 8:
                        gamma_row.append(data[i][(9 * j) + k])
                    elif k == 9:
                        sigma_row.append(data[i][(9 * j) + k])

            # Add row data to assigned list
            theta_slow.append(tslow_row)
            theta_fast.append(tfast_row)
            theta_total.append(ttotal_row)
            alpha_slow.append(aslow_row)
            alpha_fast.append(afast_row)
            alpha_total.append(atotal_row)
            beta.append(beta_row)
            gamma.append(gamma_row)
            sigma.append(sigma_row)

        # Write seperate csv files for each form of data
        write_csv(name+'_ThetaSlow.csv',theta_slow)
        write_csv(name+'_ThetaFast.csv',theta_fast)
        write_csv(name+'_ThetaTotal.csv',theta_total)
        write_csv(name+'_AlphaSlow.csv',alpha_slow)
        write_csv(name+'_AlphaFast.csv',alpha_fast)
        write_csv(name+'_AlphaTotal.csv',alpha_total)
        write_csv(name+'_Beta.csv',beta)
        write_csv(name+'_Gamma.csv',gamma)
        write_csv(name+'_Sigma.csv',sigma)

#=============================FORMATTING========================================

# formatting-getting rid of the empty spaces
def first_row_format(lst,char):
    while len(lst) != 2:
        lst.remove(char)
    return lst

def data_format(lst,chans, datatype):

    if datatype.upper() == 'FNIRS':
        for i in range(len(lst)-2):
            for j in range(chans*2):
                lst[i+2][j] = float(lst[i+2][j])
        return lst

    elif datatype.upper() == 'EEG':
        for i in range(len(lst)-1):
            for j in range(chans*9):
                lst[i+1][j] = float(lst[i+1][j])
        return lst

    elif (datatype.upper() == 'ECG' or datatype.upper() == 'EDA' or datatype.upper() == 'RESPIRATION'):
        for i in range(len(lst)-1):
            for j in range(chans):
                lst[i+1][j] = float(lst[i+1][j])
        return lst

        # elif datatype.upper() == 'GSR':
    #     for i in range(len(lst)-2):
    #         for j in range(chans*1):
    #             if lst[i+2][j] == "":
    #               continue
    #             else:
    #               lst[i+2][j] = float(lst[i+2][j])
        # return lst
    # LATER ON IMPLEMENT STUFF FOR BLANKS

def cond_format(lst):
    empt = lst[0][0]
    for i in range(len(lst)):
        while lst[i].count(empt) != 0:
            lst[i].remove(empt)
    for i in range(len(lst)-1):
        for j in range(len(lst[i+1])-2):
            lst[i+1][j+2] = int(lst[i+1][j+2])
    return lst

#returns the Data Type as a string(eg. fNIRS) upon being given the name of an all data file
#The format should be SUBJECTNUMBER_SENSOR_....csv
def getDataType(name):
    firstUnderscore = False
    for i in range(len(name)):
        firstUnderscore = name[i] == '_'
        if(firstUnderscore):
            DataType = ""
            ch = name[i + 1]
            while ch != "_":
                DataType += ch
                i += 1
                ch = name[i + 1]
            print(DataType)
            return DataType
#returns the subject Number(eg. 2002) upon being given the name of an all data file
#The format should be SUBJECTNUMBER_SENSOR_....csv
def getSubjectNumber(name):
    subject_number = ""
    for ch in name:
        if(ch == '_'):
            return subject_number
        subject_number += ch

#Given a list of Files, it groups the files into their subjects.
#The file format should be SENSOR_SUBJECTNUMBER.csv
def groupSubjects(Files):
    Subjects = []
    while Files:
        #print("LOOP")
        subject = []
        cur = getSubjectNumber(Files[0])
        for item in Files:
            if getSubjectNumber(item) == cur:
                subject.append(item)
        for item in subject:
            Files.remove(item)
        Subjects.append(subject)
    return Subjects

#Used to get the attribute count of an arff file
def getAttributeCount(arff):
    total = 0
    with open(arff) as f:
        for line in f:
            if line[0:2] == "@A":
                total += 1
    return total - 1
    #Subtracting one to remove "@ATTRIBUTE conditions" from the count

#==========================FILE CONCATENATION===================================

#Concatenate takes Arff Files and combines them
def concatenate(num_subjects, Subjects, length, name):
    all_data= []
    for i in range(num_subjects):
        cur = []
        #Concatenate is used on already used files so the name of the file will be
        #something line fuse_2002_Arff.arff
        with open("fuse_" + getSubjectNumber(Subjects[i][0]) + "_Arff.arff") as f:
            for line in f:
                cur.append(line)
            if (i != 0):
                for j in range(length): # LENGTH WILL BE TOTAL ARFFLINES
                    cur.pop(0)
            all_data += cur

        with open(name, 'wb') as f:
            for i in range(len(all_data)):
                f.writelines(all_data[i])

#Fuses the arff files for diffrent Data types
def combineDataTypes(Data, numChans):
    All_Data = []
    for i in range (len(Data)):
        arffLine[getDataType(Data[i])] = getAttributeCount(Data[i]) / numChans[getDataType(Data[i])]

    print(arffLine)

    for i in range(len(Data)):
        cur = []
        with open(Data[i]) as f:
            for line in f:
                cur.append(line)

        #The first line in an Arff file is @Relation ...
        if i == 0:
            All_Data.append(cur[0])
        cur.pop(0)

        #Copy all of the attributes from each sensors Arff to the all_data
        for x in range(arffLine[getDataType(Data[i])] * numChans[getDataType(Data[i])]):
            All_Data.append(cur[0])
            cur.pop(0)

        #Add The two lines after the attributes
        DataLines = 0
        if i == len(Data) - 1:
            All_Data.append(cur[0])
            cur.pop(0)
            All_Data.append(cur[0])
            cur.pop(0)
            print("CUR NOW")
            #Calculate the # of instances
            while cur:
                cur.pop(0)
                DataLines += 1

    #Calculate the # of attributes in the new arff file
    arffLines = 0
    for line in All_Data:
        arffLines += 1

    #Add a new line in the array for the number of instances
    for i in range(DataLines):
        All_Data.append("")

    #remove the condition number from the end of all of the instances except for the last
    #one and fuse them.
    for i in range(len(Data)):
        print(i)
        cur = []
        with open(Data[i]) as f:
            for line in f:
                cur.append(line)
        for z in range(arffLine[getDataType(Data[i])] * numChans[getDataType(Data[i])] + 3):
            cur.pop(0)
        print("LEN of DATALINES: ", DataLines)
        for x in range(DataLines):
            lineAdding = cur[x]
            if i != (len(Data) - 1) and x % 2 == 0:
                All_Data[arffLines + x] += lineAdding[0:len(lineAdding) - 3]
            else:
                All_Data[arffLines + x] += lineAdding

    #Write the fused arff file
    name = "fuse_" + getSubjectNumber(Data[0]) + "_Arff.arff"
    with open((name),'wb') as f:
        for i in range(len(All_Data)):
            f.writelines(All_Data[i])

    #Calculate and returns the number of attributes in the arff file for use later
    length = 0
    for z in range(len(Data)):
        length += arffLine[getDataType(Data[z])] * numChans[getDataType(Data[z])]
    length += 3

    return length

def pairROI(num, files):
    name = "ROI_file_" + str(num[0]) + "000s.txt"
    if name not in files:
        print("ERROR: NO ROI FILE TO MATCH SUBJECT " + num)
    else:
        return name

def arffToTab(arff_name):
    print("CREATING TAB FILE")

    convert(arff_name)

    print("TAB FILE CREATED")

#===============================================================================
#===========================RUNNING EVERYTHING==================================
#===============================================================================

#Server_URL paramater edited out
def run(server_url, local, subject,num_k,n_num,Conditions,fNIRS_ZScore, EEG_ZScore, Respiration_ZScore, EDA_ZScore, ECG_ZScore, ROI,Extension,Each_Tab,
        fNIRS_SAX, fNIRS_SAX_Word, fNIRS_SAX_Letter,
        EEG_SAX, EEG_SAX_Word, EEG_SAX_Letter,
        Respiration_SAX, Respiration_SAX_Word, Respiration_SAX_Letter,
        EDA_SAX, EDA_SAX_Word, EDA_SAX_Letter,
        ECG_SAX, ECG_SAX_Word, ECG_SAX_Letter, Each_ML, top_features, pseudo_sampling,
        ECG_sampling_rate, EDA_sampling_rate, Resp_sampling_rate, fNIRS_ROI_Filenames):

    print("STARTED RUNNING")

    #Dictionary for the number of channels in each data type
    numChans = {}

    #Gets the number of chans for each data type in this subject
    for data_name in subject:
        print(local)
        if(local):
            print("RUNNING LOCAL")
            data = open_csv(data_name)
        else:
            print("RUNNING ON SERVER")
            data = open_url(server_url, data_name)
        datatype = getDataType(data_name)
        if datatype.upper() == "FNIRS":
            #print(len(data[0]))
            numChans[datatype] = len(data[0])/2 #split for oxy/deoxy
        elif datatype.upper() == "EEG":
            numChans[datatype] = len(data[0])/9 #split for the 9 data types (eg. thetaslow, etc)
        elif datatype.upper() == 'EDA' or 'ECG' or 'RESPIRATION':
            numChans[datatype] = 1
        #get number of channels for other data types
    #Runs for each individual file
    for data_name in subject:
        datatype = getDataType(data_name)
        head = getSubjectNumber(data_name)
        conds_name = head + '_' + datatype +'_conditions.csv' #EDITED FROM head + '_Conditions_valence'

#==========================INPUTTING DATA FILES=================================
        print("OPENING FILES")

        # open files
        data = open_csv(data_name) #EDITED from open_url
        #conds = open_url(server_url,conds_name)
        conds = open_csv(conds_name)
        num_chans = numChans[datatype]
        # separates total data into separate oxy and deoxy files, to be used
        # in the arff file generator and then Orange
        data = data_format(data,num_chans,datatype)
        conds = cond_format(conds)
        num_conds = (len(conds)-1)/2

        print("FILES OPENED")

    #===========================Z-SCORING THE DATA==================================

        # NOTE: This section is optional, might not be used every time

        if datatype.upper() == 'FNIRS' and fNIRS_ZScore:
            print("Z Scored fNIRS")
            for j in range(num_chans*2):
                zary = []
                for i in range(len(data)-2):
                    zary.append(data[i+2][j])
                zary = stats.zscore(zary)
                for i in range(len(data)-2):
                    data[i+2][j] = zary[i]

        elif datatype.upper() == 'EEG' and EEG_ZScore:
            print("Z Scored EEG")
            for j in range(num_chans*9):
                zary = []
                for i in range(len(data)-9):
                    zary.append(data[i+9][j])
                zary = stats.zscore(zary)
                for i in range(len(data)-9):
                    data[i+9][j] = zary[i]

        elif datatype.upper() == "RESPIRATION" and Respiration_ZScore:
            for j in range(num_chans):
                zary = []
                for i in range(len(data)-1):
                    zary.append(data[i+1][j])
                zary = stats.zscore(zary)
                for i in range(len(data)-1):
                    data[i+1][j] = zary[i]
            print("This should not print. Keep Respiration ZScore false for now")

        elif datatype.upper() == "EDA" and EDA_ZScore:
            for j in range(num_chans):
                zary = []
                for i in range(len(data)-2):
                    zary.append(data[i+2][j])
                zary = filter(lambda x:x !="", zary) # remove empty spaces
                zary = stats.zscore(zary)
                for i in range(len(data)-5): # 5 to account for 2 rows of labels and 2
                    data[i+2][j] = zary[i]      # empty spaces
            print ("This should also not print. EDA zscore should be false for now.")

        elif datatype.upper() == "ECG" and ECG_ZScore:
            for j in range(num_chans):
                zary = []
                for i in range(len(data)-1):
                    zary.append(data[i+1][j])
                zary = stats.zscore(zary)
                for i in range(len(data)-1):
                    data[i+1][j] = zary[i]

            #when we have it, write ecg zscore here
            print ("why is ecg zscore true???")


    #=======================REGION OF INTEREST ANALYSIS=============================

        # NOTE: This section is optional, might not be used every time
        if ROI and datatype.upper() == "FNIRS":
            print("ROI")
            # Reading the ROI lines from a file
            ROI_lines = []
            #with open('ROI_'+head+'.txt','rb') as f:
            ROIName = pairROI(head, fNIRS_ROI_Filenames)
            with open(ROIName) as f:
                for line in f:
                    row = []
                    num = ""
                    for i in range(len(line)):
                        if line[i] != ',':
                            num += line[i]
                        else:
                            row.append(int(num))
                            num = ""
                    row.append(int(num[:len(num)-1]))
                    ROI_lines.append(row)
                num_chans = len(ROI_lines)

            # Producing a new ROIized data table
            firstl = ['Oxy'] + ['']*(num_chans-1)+['Deoxy']+['']*(num_chans-1)
            secondl = []
            for i in range(num_chans):
                secondl += [('CH'+str(i+1))]
            new_data = []
            for i in range(len(data)-2):
                oxy = []
                deoxy = []
                for line in ROI_lines:
                    aveo = 0
                    aved = 0
                    for j in range(len(line)):
                        aveo += data[i+2][line[j]-1]
                        aved += data[i+2][line[j]+num_chans-1]
                    oxy.append(float(aveo)/len(line))
                    deoxy.append(float(aved)/len(line))
                new_data.append((oxy+deoxy))
            data = [firstl,secondl*2]
            data+=new_data
            #Updates the number of channels for fNIRS data after the ROI analysis
            numChans["fNIRS"] = len(data[0])/2

#========================CONVERTING TO MARKS FILE===============================
        print("CONVERTING TO MARKS FILES")

        # Separate the oxy and deoxy data for the arff file generator
        write_sep_data(data,num_chans,head +'_' + datatype,datatype)
        marks = [['start','end','condition']]
        for i in range(num_conds+1):
            #print("Num_conds :" + str(num_conds))
            #if i == 0 or Conditions.find(str(i)) == -1:
            if i == 0 or str(i) not in Conditions:
                #print("NOT IN" + str(i))
                continue
            for j in range(len(conds[i*2])-2):
                row = [str(conds[i*2-1][j+2]),
                       str(conds[i*2-1][j+2]+conds[i*2][j+2]),
                       str(i)]
                marks.append(row)

        # formats the Conditions file into a [starts,ends, condition] file to
        # be used in the arff file generator
        write_csv(head + '_' + datatype +'_Marks.csv',marks)

        print("CONVERTED TO MARKS FILE")

#========================PASSING TO ARFFGEN====================================
# arff file generator passed in, pass 1 into subjects until further notice (Comment from summer 2015)

        # Diffrent Datatypes can have diffrent arff values for SAX
        if datatype == "fNIRS":
            arff_generate(head + '_' + datatype,num_conds,1,num_chans,Conditions,
                      fNIRS_SAX, fNIRS_SAX_Word, fNIRS_SAX_Letter, pseudo_sampling)

        elif datatype == "EEG":
            arff_generate(head + '_' + datatype,num_conds,1,num_chans,Conditions,
                      EEG_SAX, EEG_SAX_Word, EEG_SAX_Letter, pseudo_sampling)

        elif datatype == "Respiration":
            arff_generate(head + '_' + datatype,num_conds,1,num_chans,Conditions,
                      Respiration_SAX, Respiration_SAX_Word, Respiration_SAX_Letter, Resp_sampling_rate)

        if datatype == "EDA":
            arff_generate(head + '_' + datatype,num_conds,1,num_chans,Conditions,
                      EDA_SAX, EDA_SAX_Word, EDA_SAX_Letter, EDA_sampling_rate)

        if datatype == "ECG":
            arff_generate(head + '_' + datatype,num_conds,1,num_chans,Conditions,
                      ECG_SAX, ECG_SAX_Word, ECG_SAX_Letter, ECG_sampling_rate)

        if Each_Tab:
            arff_name = head + '_' + datatype + '_Arff'
            arffToTab(arff_name)

        print("PASSED TO ARFF GEN")

#=============================PASSING IN ORANGE=================================


    print("PASSING TO ORANGE")

    #Creates an array of arff files for each sensor in the subject to be fused
    Arffs = []
    for item in subject:
        name = getSubjectNumber(item) + '_' + getDataType(item) + "_Arff.arff"
        print(name)
        Arffs.append(name)

    #combineDataTypes returns the # of attributes
    length = combineDataTypes(Arffs, numChans)

    if Each_Tab:
        arff_name = "fuse_" + head + "_Arff"
        print arff_name
        arffToTab(arff_name)

    if Each_ML:
        #if Each_ML is true run machine learning
        print ("runing individual machine learning on " + head)
        write_csv((head+'_ML_Data'+Extension),orange("fuse_" + head + "_Arff.arff",num_k,n_num, top_features))
    else:
        print ("did not run individual machine learning")

    return length

    print("PASSED TO ORANGE")

#===============================================================================
#=================================MAIN==========================================
#===============================================================================


def main():
    #==============================USER INPUTS======================================

        ################################################################################
    # DEFAULT PARAMETERS/VALUES & DATA FILENAMES                                   #
    ################################################################################

    # Sensors
    fNIRS = False
    EEG = False
    Respiration = False
    ECG = False
    EDA = False

    # Feature Parameters
    fNIRS_ZScore = False
    fNIRS_ROI = False
    fNIRS_ROI_Filenames = []
    EEG_ZScore = False
    Respiration_ZScore = False
    Respiration_Sampling_Rate = 1000
    ECG_ZScore = False
    ECG_Sampling_Rate = 1000
    EDA_ZScore = False
    EDA_Sampling_Rate = 1000
    pseudo_sampling = 0 # passed to arff gen as filler for fNIRs and EEG

    # SAX Parameters
    fNIRS_SAX = False
    fNIRS_SAX_Word = 0
    fNIRS_SAX_Letter = 0
    EEG_SAX = False
    EEG_SAX_Word = 0
    EEG_SAX_Letter = 0
    Respiration_SAX = False
    Respiration_SAX_Word = 0
    Respiration_SAX_Letter = 0
    ECG_SAX = False
    ECG_SAX_Word = 0
    ECG_SAX_Letter = 0
    EDA_SAX = False
    EDA_SAX_Word = 0
    EDA_SAX_Letter = 0

    # Machine Learning Parameters
    Conditions = ['1', '2']
    num_k = 10
    n_num = 100
    top_features = [1]

    # Output
    Each_arff = False
    All_arff = False
    Each_Tab = False
    All_Tab = False
    Each_ML = False
    All_ML = False

    Extension = '.csv'

    # Data Files
    fNIRS_Data_Filenames = []
    EEG_Data_Filenames = []
    Respiration_Data_Filenames = []
    ECG_Data_Filenames = []
    EDA_Data_Filenames = []

    Local = True
    URL = ''


    ################################################################################
    # PARAMETERS                                                                   #
    # Read-in the parameters from the text file                                    #
    ################################################################################

    # Check if parameters file exists
    try:
       fh = open("parameters.txt", "r")
    except IOError:
       sys.exit("ERROR: Can\'t find file or read data \'parameters.txt\'.")
    else:
       fh.close()

    with open('parameters.txt', 'r') as f:
        # Bool to keep track of whether there are errors.
        error_bool = False

        print("Reading in parameters from text file...")

        #-REGULAR EXPRESSIONS------------------------------------------------------#

        # General Boolean Regular Expressions
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # either 'true' or 'false', then any number of whitespace characters.
        # Also is case-insensitive (for the purpose of 'true' and 'false').
        # (e.g. 'true' or 'TRUE' or 'True')
        boolRE = re.compile('[\s\w\-]+:\s*(?P<boolean>true|false)\s*$', re.IGNORECASE)

        # General Int Regular Expression
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # at least one digit, then any number of whitespace characters.
        intRE = re.compile('[\s\w\-]+:\s*(?P<integer>\d+)\s*$')

        # SAX Letter Regular Expression
        # Modified to make sure integer value between 3 and 20
        SAXLetterRE = re.compile('[\s\w\-]+:\s*(?P<integer>([4-9])|(1[0-9]))\s*$')

        # Conditions Regular Expression
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # at least one digit, then any number of a group of one comma ',',
        # followed by any number of whitespace, followed by at least one
        # digit. Finished off by any number of whitespace characters.
        condsRE = re.compile('[\s\w\-]+:\s*(?P<conditions>\d+(,\s*\d+)*)\s*$')

        # Top Features Regular Expression
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # at least one digit, followed by a forward slash '/', then at least
        # one digit, then any number of a group of one comma ',', followed
        # by any number of whitespace, followed by at least one digit, followed
        # by a forward slash '/', followed by at least one digit. Finished
        # off by any number of whitespace characters.
        featureRE = re.compile('[\s\w\-]+:\s*(?P<top_features>\d+/\d+(,\s*\d+/\d+)*)\s*$')

        # Extension Regular Expression
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # at least one digit, then any number of a group of any number of
        # alphanumeric characters, followed by '.csv'. Finished off by
        # any number of whitespace characters.
        extRE = re.compile('[\s\w\-]+:\s*(?P<extension>\w*\.csv)\s*$')

        # ROI Files Regular Expression
        # Checks for at least one whitespace or alphanumeric character or
        # dash '-', then a colon ':', then any number of whitespace, then
        # at any number of alphanumeric characters, then 'roi' in any case,
        # then any number of alphanumeric characters, then '.txt', followed
        # by any number of a group of one comma ',', then any number of
        # whitespace, then at any number of alphanumeric characters, then
        # 'roi' in any case, then any number of alphanumeric characters,
        # then '.txt' Finished off by any number of whitespace characters.
        # Also is case-insensitive.
        ROIfilenameRE = re.compile('[\s\w\-\(\)]+:\s*(?P<filenames>\w*roi\w*\.txt(,\s*\w*roi\w*\.txt)*)\s*$', re.IGNORECASE)

        # Checks for at least one digit in name of filenames
        DigitCheckRE = re.compile('[\s\w\-\(\)]+:\s*\w*\d+\w*\.csv(,\s*\w*\d+\w*\.csv)*\s*$')
        DigitCheckTXTRE = re.compile('[\s\w\-\(\)]+:\s*\w*\d+\w*\.txt(,\s*\w*\d+\w*\.txt)*\s*$')


        #-SENSORS------------------------------------------------------------------#

        # Sensors Title
        f.readline()

        # Check if fNIRS selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                fNIRS = True
            elif (boolean.lower() == "false"):
                fNIRS = False
        else:
            print("ERROR: Invalid fNIRS Boolean Value.")
            error_bool = True

        # Check if EEG selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                EEG = True
            elif (boolean.lower() == "false"):
                EEG = False
        else:
            print("ERROR: Invalid EEG Boolean Value.")
            error_bool = True

        # Check if Respiration selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                Respiration = True
            elif (boolean.lower() == "false"):
                Respiration = False
        else:
            print("ERROR: Invalid Respiration Boolean Value.")
            error_bool = True

        # Check if ECG selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                ECG = True
            elif (boolean.lower() == "false"):
                ECG = False
        else:
            print("ERROR: Invalid ECG Boolean Value.")
            error_bool = True

        # Check if EDA selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                EDA = True
            elif (boolean.lower() == "false"):
                EDA = False
        else:
            print("ERROR: Invalid EDA Boolean Value.")
            error_bool = True


        #-FEATURE PARAMETERS-------------------------------------------------------#

        # Empty Line
        f.readline()
        # Feature Parameters title
        f.readline()

        # If fNIRS selected
        if (fNIRS):
            # Check if fNIRS Z-Score selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    fNIRS_ZScore = True
                elif (boolean.lower() == "false"):
                    fNIRS_ZScore = False
            else:
                print("ERROR: Invalid fNIRS Z-Score Boolean Value.")
                error_bool = True

            # Check if fNIRS ROI selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    fNIRS_ROI = True
                elif (boolean.lower() == "false"):
                    fNIRS_ROI = False
            else:
                print("ERROR: Invalid fNIRS ROI Boolean Value.")
                error_bool = True

            if (fNIRS_ROI):
                # Retrieve fNIRS ROI Filenames
                line = f.readline()
                match = ROIfilenameRE.match(line)
                match2 = DigitCheckTXTRE.match(line)
                # If proper match of multiple filenames separated by commas
                if (match and match2):
                    ROI_filenames = match.group("filenames")
                    # Finds all filenames and puts them in a list
                    fNIRS_ROI_filenames_list = re.findall('\w+\.txt', ROI_filenames)
                    fNIRS_ROI_Filenames = fNIRS_ROI_filenames_list
                else:
                    print("ERROR: Invalid fNIRS ROI Filenames Format")
                    error_bool = True
            # 1 line of fNIRS ROI parameter that is unnecessary
            # if fNIRS ROI is not selected
            else:
                line = f.readline()
        # 3 lines of fNIRS parameters that are unnecessary if
        # fNIRS is not selected
        else:
            f.readline()
            f.readline()
            f.readline()

        # If EEG selected
        if (EEG):
            # Check if EEG Z-Score selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    EEG_ZScore = True
                elif (boolean.lower() == "false"):
                    EEG_ZScore = False
            else:
                print("ERROR: Invalid EEG Z-Score Boolean Value.")
                error_bool = True
        # 1 line of EEG parameters that are unnecessary if
        # EEG is not selected
        else:
            f.readline()

        # If Respiration selected
        if (Respiration):
            # Check if Respiration Z-Score selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    Respiration_ZScore = True
                elif (boolean.lower() == "false"):
                    Respiration_ZScore = False
            else:
                print("ERROR: Invalid Respiration Z-Score Boolean Value.")
                error_bool = True
            # Retrieve Respiration Sampling Rate
            line = f.readline()
            match = intRE.match(line)
            # If proper match of integers
            if (match):
                integer = match.group("integer")
                Respiration_Sampling_Rate = int(integer)
            else:
                print("ERROR: Invalid Respiration Sampling Rate Integer Value.")
                error_bool = True
        # 2 lines of Respiration parameters that are unnecessary if
        # Respiration is not selected
        else:
            f.readline()
            f.readline()

        # If ECG selected
        if (ECG):
            # Check if ECG Z-Score selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    ECG_ZScore = True
                elif (boolean.lower() == "false"):
                    ECG_ZScore = False
            else:
                print("ERROR: Invalid ECG Z-Score Boolean Value.")
                error_bool = True
            # Retrieve ECG Sampling Rate
            line = f.readline()
            match = intRE.match(line)
            # If proper match of integers
            if (match):
                integer = match.group("integer")
                ECG_Sampling_Rate = int(integer)
            else:
                print("ERROR: Invalid ECG Sampling Rate Integer Value.")
                error_bool = True
        # 2 lines of ECG parameters that are unnecessary if
        # ECG is not selected
        else:
            f.readline()
            f.readline()

        # If EDA selected
        if (EDA):
            # Check if EDA Z-Score selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    EDA_ZScore = True
                elif (boolean.lower() == "false"):
                    EDA_ZScore = False
            else:
                print("ERROR: Invalid EDA Z-Score Boolean Value.")
                error_bool = True
            # Retrieve EDA Sampling Rate
            line = f.readline()
            match = intRE.match(line)
            # If proper match of integers
            if (match):
                integer = match.group("integer")
                EDA_Sampling_Rate = int(integer)
            else:
                print("ERROR: Invalid EDA Sampling Rate Integer Value.")
                error_bool = True
        # 2 lines of EDA parameters that are unnecessary if
        # EDA is not selected
        else:
            f.readline()
            f.readline()


        #-SAX PARAMETERS-----------------------------------------------------------#

        # Empty Line
        f.readline()
        # SAX Parameters title
        f.readline()

        # If fNIRS selected
        if (fNIRS):
            # Check if fNIRS SAX selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    fNIRS_SAX = True
                elif (boolean.lower() == "false"):
                    fNIRS_SAX = False
            else:
                print("ERROR: Invalid fNIRS SAX Boolean Value.")
                error_bool = True

            if (fNIRS_SAX):
                # Retrieve fNIRS SAX Word Value
                line = f.readline()
                match = intRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    fNIRS_SAX_Word = int(integer)
                else:
                    print("ERROR: Invalid fNIRS SAX Word Integer Value.")
                    error_bool = True
                # Retrieve fNIRS SAX Letter Value
                line = f.readline()
                match = SAXLetterRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    fNIRS_SAX_Letter = int(integer)
                else:
                    print("ERROR: Invalid fNIRS SAX Letter Integer Value. (Must be between 3 and 20)")
                    error_bool = True
            # 2 lines of fNIRS SAX parameters that are unnecessary
            # if fNIRS SAX is not selected
            else:
                f.readline()
                f.readline()
        # 3 lines of fNIRS SAX parameters that are unnecessary if
        # fNIRS is not selected
        else:
            f.readline()
            f.readline()
            f.readline()

        # If EEG selected
        if (EEG):
            # Check if EEG SAX selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    EEG_SAX = True
                elif (boolean.lower() == "false"):
                    EEG_SAX = False
            else:
                print("ERROR: Invalid EEG SAX Boolean Value.")
                error_bool = True

            if (EEG_SAX):
                # Retrieve EEG SAX Word Value
                line = f.readline()
                match = intRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    EEG_SAX_Word = int(integer)
                else:
                    print("ERROR: Invalid EEG SAX Word Integer Value.")
                    error_bool = True
                # Retrieve EEG SAX Letter Value
                line = f.readline()
                match = SAXLetterRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    EEG_SAX_Letter = int(integer)
                else:
                    print("ERROR: Invalid EEG SAX Letter Integer Value. (Must be between 3 and 20)")
                    error_bool = True
            # 2 lines of EEG SAX parameters that are unnecessary
            # if EEG SAX is not selected
            else:
                f.readline()
                f.readline()
        # 3 lines of EEG SAX parameters that are unnecessary if
        # EEG is not selected
        else:
            f.readline()
            f.readline()
            f.readline()

        # If Respiration selected
        if (Respiration):
            # Check if Respiration SAX selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    Respiration_SAX = True
                elif (boolean.lower() == "false"):
                    Respiration_SAX = False
            else:
                print("ERROR: Invalid Respiration SAX Boolean Value.")
                error_bool = True

            if (Respiration_SAX):
                # Retrieve Respiration SAX Word Value
                line = f.readline()
                match = intRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    Respiration_SAX_Word = int(integer)
                else:
                    print("ERROR: Invalid Respiration SAX Word Integer Value.")
                    error_bool = True
                # Retrieve Respiration SAX Letter Value
                line = f.readline()
                match = SAXLetterRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    Respiration_SAX_Letter = int(integer)
                else:
                    print("ERROR: Invalid Respiration SAX Letter Integer Value. (Must be between 3 and 20)")
                    error_bool = True
            # 2 lines of Respiration SAX parameters that are unnecessary
            # if Respiration SAX is not selected
            else:
                f.readline()
                f.readline()
        # 3 lines of Respiration SAX parameters that are unnecessary if
        # Respiration is not selected
        else:
            f.readline()
            f.readline()
            f.readline()

        # If ECG selected
        if (ECG):
            # Check if ECG SAX selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    ECG_SAX = True
                elif (boolean.lower() == "false"):
                    ECG_SAX = False
            else:
                print("ERROR: Invalid ECG SAX Boolean Value.")
                error_bool = True

            if (ECG_SAX):
                # Retrieve ECG SAX Word Value
                line = f.readline()
                match = intRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    ECG_SAX_Word = int(integer)
                else:
                    print("ERROR: Invalid ECG SAX Word Integer Value.")
                    error_bool = True
                # Retrieve ECG SAX Letter Value
                line = f.readline()
                match = SAXLetterRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    ECG_SAX_Letter = int(integer)
                else:
                    print("ERROR: Invalid ECG SAX Letter Integer Value. (Must be between 3 and 20)")
                    error_bool = True
            # 2 lines of ECG SAX parameters that are unnecessary
            # if ECG SAX is not selected
            else:
                f.readline()
                f.readline()
        # 3 lines of ECG parameters that are unnecessary if
        # ECG is not selected
        else:
            f.readline()
            f.readline()
            f.readline()

        # If EDA selected
        if (EDA):
            # Check if EDA SAX selected
            line = f.readline()
            match = boolRE.match(line)
            # If proper match of true or false
            if (match):
                boolean = match.group("boolean")
                if (boolean.lower() == "true"):
                    EDA_SAX = True
                elif (boolean.lower() == "false"):
                    EDA_SAX = False
            else:
                print("ERROR: Invalid EDA SAX Boolean Value.")
                error_bool = True

            if (EDA_SAX):
                # Retrieve EDA SAX Word Value
                line = f.readline()
                match = intRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    EDA_SAX_Word = int(integer)
                else:
                    print("ERROR: Invalid EDA SAX Word Integer Value.")
                    error_bool = True
                # Retrieve EDA SAX Letter Value
                line = f.readline()
                match = SAXLetterRE.match(line)
                # If proper match of integers
                if (match):
                    integer = match.group("integer")
                    EDA_SAX_Letter = int(integer)
                else:
                    print("ERROR: Invalid EDA SAX Letter Integer Value. (Must be between 3 and 20)")
                    error_bool = True
            # 2 lines of EDA SAX parameters that are unnecessary
            # if EDA SAX is not selected
            else:
                f.readline()
                f.readline()
        # 3 lines of EDA parameters that are unnecessary if
        # EDA is not selected
        else:
            f.readline()
            f.readline()
            f.readline()


        #-MACHINE LEARNING PARAMETERS----------------------------------------------#

        # Empty Line
        f.readline()
        # Machine Learning Parameters title
        f.readline()

        # Retrieve conditions to be checked
        line = f.readline()
        match = condsRE.match(line)
        # If proper match of multiple integers separated by commas
        if (match):
            conds = match.group("conditions")
            # Finds all condition numbers (string ints) and puts them in a list
            conds_list = re.findall('\d+', conds)
            # Convert all the 'string ints' in the list to actual ints
            #conds_list = map(int, conds_list)
            Conditions = conds_list
        else:
            print("ERROR: Invalid Conditions Values")
            error_bool = True

        # Retrieve num_k
        line = f.readline()
        match = intRE.match(line)
        # If proper match of integers
        if (match):
            integer = match.group("integer")
            num_k = int(integer)
        else:
            print("ERROR: Invalid num_k Integer Value.")
            error_bool = True

        # Retrieve n_num
        line = f.readline()
        match = intRE.match(line)
        # If proper match of integers
        if (match):
            integer = match.group("integer")
            n_num = int(integer)
        else:
            print("ERROR: Invalid n_num Integer Value.")
            error_bool = True

        # Retrieve top features
        line = f.readline()
        match = featureRE.match(line)
        # If proper match of multiple fractions separated by commas
        if (match):
            top_features = match.group("top_features")
            # Finds all fraction denominators (string ints) and puts them in a list
            top_features_list = re.findall('(?<=/)\d+', top_features)
            # Convert all the 'string ints' in the list to actual ints
            top_features_list = map(int, top_features_list)
            top_features = top_features_list
        else:
            print("ERROR: Invalid Top Features Values")
            error_bool = True


        #-OUTPUT-------------------------------------------------------------------#

        # Empty Line
        f.readline()
        # Output title
        f.readline()

        # Check if Each ARFF is selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                Each_arff = True
            elif (boolean.lower() == "false"):
                Each_arff = False
        else:
            print("ERROR: Invalid Each_arff Boolean Value.")
            error_bool = True

        # Check if All ARFF is selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                All_arff = True
            elif (boolean.lower() == "false"):
                All_arff = False
        else:
            print("ERROR: Invalid All_arff Boolean Value.")
            error_bool = True

        # Check if Each Tab is selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                Each_Tab = True
            elif (boolean.lower() == "false"):
                Each_Tab = False
        else:
            print("ERROR: Invalid Each_Tab Boolean Value.")
            error_bool = True

        # Check if All Tab is selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                All_Tab = True
            elif (boolean.lower() == "false"):
                All_Tab = False
        else:
            print("ERROR: Invalid All_Tab Boolean Value.")
            error_bool = True

        # Check if Each ML is selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                Each_ML = True
            elif (boolean.lower() == "false"):
                Each_ML = False
        else:
            print("ERROR: Invalid Each_ML Boolean Value.")
            error_bool = True

        # Check if All ML is selected
        line = f.readline()
        match = boolRE.match(line)
        # If proper match of true or false
        if (match):
            boolean = match.group("boolean")
            if (boolean.lower() == "true"):
                All_ML = True
            elif (boolean.lower() == "false"):
                All_ML = False
        else:
            print("ERROR: Invalid All_ML Boolean Value.")
            error_bool = True

        # Empty Line
        f.readline()

        # Retrieve extension
        line = f.readline()
        match = extRE.match(line)
        # If proper match of multiple integers separated by commas
        if (match):
            Extension = match.group("extension")
        else:
            print("ERROR: Invalid Extension")
            error_bool = True

        #Retrieve URL info

        f.readline()
        LocalCur = f.readline()[8:]
        if "False" in LocalCur:
            Local = False
        elif "True" in LocalCur:
            Local = True
        else:
            print("ERROR: Local variable must be a bool")
        URL = f.readline()[6:]

        #-ERROR HANDLING-----------------------------------------------------------#

        if (error_bool):
            sys.exit()
        else:
            print("Successfully read-in parameters from text file.")


        #-TESTS--------------------------------------------------------------------#
        print("fNIRS: ", fNIRS)
        print("EEG: ", EEG)
        print("Respiration: ", Respiration)
        print("ECG: ", ECG)
        print("EDA: ", EDA)
        print("fNIRS_ZScore: ", fNIRS_ZScore)
        print("fNIRS_ROI: ", fNIRS_ROI)
        print("fNIRS_ROI_Filenames: ", fNIRS_ROI_Filenames)
        print("EEG_ZScore: ", EEG_ZScore)
        print("Respiration_ZScore: ", Respiration_ZScore)
        print("Respiration_Sampling_Rate: ", Respiration_Sampling_Rate)
        print("ECG_ZScore: ", ECG_ZScore)
        print("ECG_Sampling_Rate: ", ECG_Sampling_Rate)
        print("EDA_ZScore: ", EDA_ZScore)
        print("EDA_Sampling_Rate: ", EDA_Sampling_Rate)
        print("fNIRS_SAX: ", fNIRS_SAX)
        print("fNIRS_SAX_Word: ", fNIRS_SAX_Word)
        print("fNIRS_SAX_Letter: ", fNIRS_SAX_Letter)
        print("EEG_SAX: ", EEG_SAX)
        print("EEG_SAX_Word: ", EEG_SAX_Word)
        print("EEG_SAX_Letter: ", EEG_SAX_Letter)
        print("Respiration_SAX: ", Respiration_SAX)
        print("Respiration_SAX_Word: ", Respiration_SAX_Word)
        print("Respiration_SAX_Letter: ", Respiration_SAX_Letter)
        print("ECG_SAX: ", ECG_SAX)
        print("ECG_SAX_Word: ", ECG_SAX_Word)
        print("ECG_SAX_Letter: ", ECG_SAX_Letter)
        print("EDA_SAX: ", EDA_SAX)
        print("EDA_SAX_Word: ", EDA_SAX_Word)
        print("EDA_SAX_Letter: ", EDA_SAX_Letter)
        print("Conditions: ", Conditions)
        print("num_k: ", num_k)
        print("n_num: ", n_num)
        print("Top Features: ", top_features)
        print("Each_arff: ", Each_arff)
        print("All_arff: ", All_arff)
        print("Each_Tab: ", Each_Tab)
        print("All_Tab: ", All_Tab)
        print("Each_ML: ", Each_ML)
        print("All_ML: ", All_ML)
        print("Extension: ", Extension)
        print("Local: ", Local)
        print("URL: ", URL)

    f.closed


    ################################################################################
    # DATA FILENAMES                                                               #
    # Read-in the data filenames from the text file                                #
    ################################################################################

    # Check if data name file exists
    try:
       fh = open("data_filenames.txt", "r")
    except IOError:
       sys.exit("ERROR: Can\'t find file or read data \'data_filenames.txt\'.")
    else:
       fh.close()

    with open('data_filenames.txt', 'r') as df:
        # Bool to keep track of whether there are errors.
        error_bool = False

        print("Reading in data filenames from text file...")

        #-REGULAR EXPRESSIONS------------------------------------------------------#

        # Data Filename Format Is STRICT
        # [/OptionalDirectories/][Subject#]_[Sensor]_All_Data.csv

        # Data Filename Regular Expression
        # Checks the format of data filenames and provides ability to extract
        # the crucial information of the directory, subject number, and sensor
        # type. Checks for one or no '/', then any number of a group of at least
        # one alphanumeric or whitespace character followed by a '/', then at
        # least one digit, followed by an underscore '_', then either 'fNIRS',
        # 'EEG', 'Respiration', 'ECG', or 'EDA' in any case, followed by an
        # underscore '_', then 'All' in any case, followed by an underscore '_',
        # then 'Data' in any case, finished with '.csv'.
        filenameRE = re.compile('(?P<directory>/?([\w\s]+/)*)(?P<filename>(?P<subject>\d+)_(?P<sensor>(fNIRS|EEG|Respiration|ECG|EDA))_All_Data\.csv)$', re.IGNORECASE)


        #-DATA FILES---------------------------------------------------------------#

        # Intiial Variables
        line_num = 0
        noexist_file_error_bool = False
        noexist_file_error_list = []
        duplicate_file_error_bool = False
        duplicate_file_error_list = []
        missing_files_error_bool = False
        missing_files_error_list = []
        file_error_bool = False
        file_error_list = []
        filename_error_bool = False
        filename_error_list = []
        subject_error_bool = False
        subject_error_list = []
        fNIRS_Subjects = []
        EEG_Subjects = []
        Respiration_Subjects = []
        ECG_Subjects = []
        EDA_Subjects = []
        SensorSets = []
        Difference = []

        # Data Files title
        df.readline()
        line_num += 1

        # Retrieve Data Filenames
        for line in df:
            # Remove leading and trailing whitespace characters
            clean_line = line.strip()
            line_num += 1
            match = filenameRE.match(clean_line)
            # Group data files accordingly and extract the subject numbers
            # for separate sensors.
            if (match):
                # Make sure the data file actually exists first.
                try:
                    testfile = open(clean_line, 'r')
                except IOError:
                    directory = match.group("directory")
                    if ((directory[:-1]) == os.getcwd() or directory == ''):
                        noexist_file_error_list.append('\'' + match.group("filename") + '\'' + " does not exist.")
                    else:
                        noexist_file_error_list.append('\'' + match.group("filename") + '\'' + " does not exist in " + directory)
                    error_bool = True
                    noexist_file_error_bool = True
                else:
                    testfile.close()
                    if (match.group("sensor").lower() == "fnirs"):
                        # Check if one or more of the same data file is provided
                        if (fNIRS_Data_Filenames.count(match.group("filename")) != 0):
                            duplicate_file_error_list.append(match.group("filename"))
                            error_bool = True
                            duplicate_file_error_bool = True
                        else:
                            fNIRS_directory = match.group("directory")
                            # Check if there is a directory provided
                            if (fNIRS_directory != ''):
                                # If data file in different directory than this program,
                                # account for this by making a copy of it in the
                                # directory of this program
                                if ((fNIRS_directory[:-1]) != os.getcwd()):
                                    shutil.copy2(clean_line, os.getcwd())
                                # Add just the filename to the list
                                fNIRS_Data_Filenames.append(match.group("filename"))
                            else:
                                fNIRS_Data_Filenames.append(clean_line)
                            fNIRS_Subjects.append(int(match.group("subject")))
                    elif (match.group("sensor").lower() == "eeg"):
                        # Check if one or more of the same data file is provided
                        if (EEG_Data_Filenames.count(match.group("filename")) != 0):
                            duplicate_file_error_list.append(match.group("filename"))
                            error_bool = True
                            duplicate_file_error_bool = True
                        else:
                            EEG_directory = match.group("directory")
                            # Check if there is a directory provided
                            if (EEG_directory != ''):
                                # If data file in different directory than this program,
                                # account for this by making a copy of it in the
                                # directory of this program
                                if ((EEG_directory[:-1]) != os.getcwd()):
                                    shutil.copy2(clean_line, os.getcwd())
                                # Add just the filename to the list
                                EEG_Data_Filenames.append(match.group("filename"))
                            else:
                                EEG_Data_Filenames.append(clean_line)
                            EEG_Subjects.append(int(match.group("subject")))
                    elif (match.group("sensor").lower() == "respiration"):
                        # Check if one or more of the same data file is provided
                        if (Respiration_Data_Filenames.count(match.group("filename")) != 0):
                            duplicate_file_error_list.append(match.group("filename"))
                            error_bool = True
                            duplicate_file_error_bool = True
                        else:
                            Respiration_directory = match.group("directory")
                            # Check if there is a directory provided
                            if (Respiration_directory != ''):
                                # If data file in different directory than this program,
                                # account for this by making a copy of it in the
                                # directory of this program
                                if ((Respiration_directory[:-1]) != os.getcwd()):
                                    shutil.copy2(clean_line, os.getcwd())
                                # Add just the filename to the list
                                Respiration_Data_Filenames.append(match.group("filename"))
                            else:
                                Respiration_Data_Filenames.append(clean_line)
                            Respiration_Subjects.append(int(match.group("subject")))
                    elif (match.group("sensor").lower() == "ecg"):
                        # Check if one or more of the same data file is provided
                        if (ECG_Data_Filenames.count(match.group("filename")) != 0):
                            duplicate_file_error_list.append(match.group("filename"))
                            error_bool = True
                            duplicate_file_error_bool = True
                        else:
                            ECG_directory = match.group("directory")
                            # Check if there is a directory provided
                            if (ECG_directory != ''):
                                # If data file in different directory than this program,
                                # account for this by making a copy of it in the
                                # directory of this program
                                if ((ECG_directory[:-1]) != os.getcwd()):
                                    shutil.copy2(clean_line, os.getcwd())
                                # Add just the filename to the list
                                ECG_Data_Filenames.append(match.group("filename"))
                            else:
                                ECG_Data_Filenames.append(clean_line)
                            ECG_Subjects.append(int(match.group("subject")))
                    elif (match.group("sensor").lower() == "eda"):
                        # Check if one or more of the same data file is provided
                        if (EDA_Data_Filenames.count(match.group("filename")) != 0):
                            duplicate_file_error_list.append(match.group("filename"))
                            error_bool = True
                            duplicate_file_error_bool = True
                        else:
                            EDA_directory = match.group("directory")
                            # Check if there is a directory provided
                            if (EDA_directory != ''):
                                # If data file in different directory than this program,
                                # account for this by making a copy of it in the
                                # directory of this program
                                if ((EDA_directory[:-1]) != os.getcwd()):
                                    shutil.copy2(clean_line, os.getcwd())
                                # Add just the filename to the list
                                EDA_Data_Filenames.append(match.group("filename"))
                            else:
                                EDA_Data_Filenames.append(clean_line)
                            EDA_Subjects.append(int(match.group("subject")))
            # If there is no match, then the format is incorrect.
            # Take note of the error and the line number.
            else:
                filename_error_list.append("On line " + str(line_num) + ": " + clean_line)
                error_bool = True
                filename_error_bool = True

        # Checks to make sure if a sensor is selected there is at least one
        # appropriate data file provided for it as well as checks to make sure
        # a data file is not provided for a sensor that is not selected.
        if (fNIRS):
            if (len(fNIRS_Data_Filenames) == 0):
                missing_files_error_list.append("fNIRS Sensor selected but no fNIRS Data File(s) are provided.")
                error_bool = True
                missing_files_error_bool = True
        else:
            if (len(fNIRS_Data_Filenames) > 0):
                file_error_list.append("fNIRS Data File provided but fNIRS is not selected.")
                error_bool = True
                file_error_bool = True
        if (EEG):
            if (len(EEG_Data_Filenames) == 0):
                missing_files_error_list.append("EEG Sensor selected but no EEG Data File(s) are provided.")
                error_bool = True
                missing_files_error_bool = True
        else:
            if (len(EEG_Data_Filenames) > 0):
                file_error_list.append("EEG Data File provided but EEG is not selected.")
                error_bool = True
                file_error_bool = True
        if (Respiration):
            if (len(Respiration_Data_Filenames) == 0):
                missing_files_error_list.append("Respiration Sensor selected but no Respiration Data File(s) are provided.")
                error_bool = True
                missing_files_error_bool = True
        else:
            if (len(Respiration_Data_Filenames) > 0):
                file_error_list.append("Respiration Data File provided but EEG is not selected.")
                error_bool = True
                file_error_bool = True
        if (ECG):
            if (len(ECG_Data_Filenames) == 0):
                missing_files_error_list.append("ECG Sensor selected but no ECG Data File(s) are provided.")
                error_bool = True
                missing_files_error_bool = True
        else:
            if (len(ECG_Data_Filenames) > 0):
                file_error_list.append("ECG Data File provided but ECG is not selected.")
                error_bool = True
                file_error_bool = True
        if (EDA):
            if (len(EDA_Data_Filenames) == 0):
                missing_files_error_list.append("EDA Sensor selected but no EDA Data File(s) are provided.")
                error_bool = True
                missing_files_error_bool = True
        else:
            if (len(EDA_Data_Filenames) > 0):
                file_error_list.append("EDA Data File provided but EDA is not selected.")
                error_bool = True
                file_error_bool = True

        # If there is more than one sensor selected, must check there are the
        # same number of data files for each sensor selected and, in addition,
        # the data files for each sensor must be for the same subject.
        if ([fNIRS, EEG, Respiration, ECG, EDA].count(True) > 1):
            # Make each list of sensor subjects into a set and append them
            # to a list
            if (fNIRS):
                SensorSets.append(set(fNIRS_Subjects))
            if (EEG):
                SensorSets.append(set(EEG_Subjects))
            if (Respiration):
                SensorSets.append(set(Respiration_Subjects))
            if (ECG):
                SensorSets.append(set(ECG_Subjects))
            if (EDA):
                SensorSets.append(set(EDA_Subjects))

            # Extracts the differences of all the Sensor Sets if there are any
            for i in range(len(SensorSets)):
                # Check the first Subject List with each other individual
                # subject lists (instead of them all together at once which
                # is not what we want)
                for i in range(len(SensorSets) - 1):
                    Difference += list(SensorSets[0].difference(SensorSets[i + 1]))
                # Reorder SensorSets list to check from the perspective
                # of each sensor
                item = SensorSets.pop(0)
                SensorSets.append(item)
            # Convert into set and back into a list and then sort the list
            # to remove duplicates and then have the subject numbers sorted nicely
            DifferenceSet = set(Difference)
            Difference = list(DifferenceSet)
            Difference.sort()
            # If there are any differences, there is clearly an error
            if (len(Difference) > 0):
                error_bool = True
                subject_error_bool = True

            # Every subject numer in Difference is a subject number that a sensor
            # is missing a data file for. Find exactly which sensor is missing
            # which subject.
            for missing_subject in Difference:
                if (fNIRS):
                    if (fNIRS_Subjects.count(missing_subject) == 0):
                        subject_error_list.append("Missing matching fNIRS data file for subject number " + str(missing_subject))
                if (EEG):
                    if (EEG_Subjects.count(missing_subject) == 0):
                        subject_error_list.append("Missing matching EEG data file for subject number " + str(missing_subject))
                if (Respiration):
                    if (Respiration_Subjects.count(missing_subject) == 0):
                        subject_error_list.append("Missing matching Respiration data file for subject number " + str(missing_subject))
                if (ECG):
                    if (ECG_Subjects.count(missing_subject) == 0):
                        subject_error_list.append("Missing matching ECG data file for subject number " + str(missing_subject))
                if (EDA):
                    if (EDA_Subjects.count(missing_subject) == 0):
                        subject_error_list.append("Missing matching EDA data file for subject number " + str(missing_subject))


        #-ERROR HANDLING-----------------------------------------------------------#

        if (error_bool):
            if(noexist_file_error_bool):
                print("ERROR: Data File(s) provided do no exist.")
                for item in noexist_file_error_list:
                    print(item)
            if(missing_files_error_bool):
                print("ERROR: No data files provided for selected sensor(s).")
                for item in missing_files_error_list:
                    print(item)
            if (file_error_bool):
                print("ERROR: Sensor for data file(s) provided is not selected.")
                for item in file_error_list:
                    print(item)
            if (duplicate_file_error_bool):
                print("ERROR: There are one or more of the same data file(s) provided.")
                for item in duplicate_file_error_list:
                    print(item)
            if (filename_error_bool):
                print("ERROR: Invalid Data Filename(s) Format in \'data_filenames.txt\'")
                for item in filename_error_list:
                    print(item)
                print("Correct format: [/OptionalDirectories/][Subject#]_[Sensor]_All_Data.csv")
                print("e.g. 0001_fNIRS_All_Data.csv or /Data/fNIRS/0001_fNIRS_All_Data.csv")
            if (subject_error_bool):
                print("ERROR: Missing Matching Sensor Subjects.")
                for item in subject_error_list:
                    print(item)
            sys.exit()
        else:
            print("Successfully read-in data filenames from text file.")


        #-TESTS--------------------------------------------------------------------#
        print("fNIRS_Data_Filenames: ", fNIRS_Data_Filenames)
        print("EEG_Data_Filenames: ", EEG_Data_Filenames)
        print("Respiration_Data_Filenames: ", Respiration_Data_Filenames)
        print("ECG_Data_Filenames: ", ECG_Data_Filenames)
        print("EDA_Data_Filenames: ", EDA_Data_Filenames)
    df.closed

    # FILE INPUTS
    Files = fNIRS_Data_Filenames + EEG_Data_Filenames + Respiration_Data_Filenames + EDA_Data_Filenames + ECG_Data_Filenames
    num_files = len(Files) # (p_end - p_start) + 1


#-------------------------------------------------------------------------------

    Subjects = groupSubjects(Files)

    print(Files)
    print(Subjects)

    # Running the single files
    for item in Subjects:
        print("THIS IS WHAT LOCAL IS BEFORE RUN:" , Local)
        heads=run(URL, Local, item,num_k,n_num,Conditions,fNIRS_ZScore, EEG_ZScore, Respiration_ZScore, EDA_ZScore, ECG_ZScore, fNIRS_ROI,Extension, Each_Tab,
             fNIRS_SAX, fNIRS_SAX_Word, fNIRS_SAX_Letter,
             EEG_SAX, EEG_SAX_Word, EEG_SAX_Letter,
             Respiration_SAX, Respiration_SAX_Word, Respiration_SAX_Letter,
             EDA_SAX, EDA_SAX_Word, EDA_SAX_Letter,
             ECG_SAX, ECG_SAX_Word, ECG_SAX_Letter, Each_ML, top_features, pseudo_sampling,
             ECG_Sampling_Rate, EDA_Sampling_Rate, Respiration_Sampling_Rate, fNIRS_ROI_Filenames)

    # Running the single concatenated file
    concatenate(len(Subjects),Subjects,heads,"Across_Subject_Data.arff") #3828 replace with heads

    print("Still Running 2")

    if All_ML:
        print ("All ML is true")
        #Writing ML Data for concatenated files
        name = 'Across_Subject_Data'  #--Maybe change this to read 'All_extension_data
        write_csv((name+'_ML_Data'+Extension),orange(name,num_k,n_num, top_features))

    print("Still Running 3")
    # Running the Leaving a file out concatenated files
    for i in range(len(Subjects)):#Edited Loop   #--Again make it run through Files
        left = []
        for z in range(len(Subjects)):
            if z != i:
                left.append(Subjects[z])
        test_set = getSubjectNumber(Subjects[i][0])
        name = "Across_Subject_Data_No_" + test_set
        concatenate(len(Subjects) - 1, left, heads, name + "_Arff.arff")
        #if All_ML is true, then run all paraticipant minus one machine learning
        if All_ML:
            print ("ALL_ML is True, running all participant minus one Machine Learning")
            write_csv(name+'_ML_Data'+Extension,
                      orange_two(test_set,num_k,n_num, top_features))
        else:
            print ("ALL_ML is False.")

    #if All_Tab is true, then create tab files for the all participant data files
    if All_Tab:
        print ("All tab is true")
        arffToTab("Across_Subject_Data")
        for item in Subjects:
            arff_file = "Across_Subject_Data_No_" + getSubjectNumber(item[0]) + "_Arff"
            arffToTab(arff_file)

    #if Each_arff is false, then delete individual arff files
    if Each_arff == False:
        print ("each_arff is false. Delete individual arff files.")
        for item in Subjects:
            for i in item:
                arff_file = str(getDataType(i)) + "_" + str(getSubjectNumber(i)) + "_Arff.arff"
                os.remove(arff_file)
            arff_file = "fuse_" + str(getSubjectNumber(item[0])) + "_Arff.arff"
            os.remove(arff_file)
    else:
        print ("each arff is true. nothing done")

    #if All_arff is false, then delete Across_Subject_Data.arff and all th Across_Subject_Data_No_Subject#.arff
    if All_arff == False:
        print ("All arff is false")
        os.remove("Across_Subject_Data.arff")
        for item in Subjects:
            arff_file = "Across_Subject_Data_No_" + getSubjectNumber(item[0]) + "_Arff.arff"
            os.remove(arff_file)
    else:
        print ("All arff is true. nothing done")


#===============================================================================
#==============================CLOSE MAIN=======================================
#===============================================================================

if __name__ == "__main__":
    main()
