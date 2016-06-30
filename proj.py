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
#   zscore, the conditions being tested,lengths for SAX, and a couple of       #
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

import numpy as np
import csv
from arffgen import arff_generate
from saxpy import SAX
from Orange_ML import orange
from Orange_ML_two import orange_two
from scipy import stats

#Dictionary that shows the len of the attributes for each sensor
#If you add or remove attributes from arffgen, change this
arffLine = {'fNIRS': 96, 'EEG': 297, 'GSR': 33}


# For accessing the data on the server (EDITED OUT)

#======================OPENING AND WRITING CSV FILES============================
#def open_url(EDITED OUT HERE)

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
    elif datatype.upper() == 'GSR':
        for i in range(len(lst)-2):
            for j in range(chans*1):
                if lst[i+2][j] == "":
                	continue
                else:
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

#returns the subject Number(eg. 2002) upon being given the name of an all data file
#The format should be SENSOR_SUBJECTNUMBER.csv
def getSubjectNumber(name):
    firstUnderscore = False
    for i in range(len(name)):
        firstUnderscore = name[i] == '_'
        if(firstUnderscore):
            number = ""
            for x in range(1,5):
                number += name[x + i]
            return number
        
#returns the Data Type as a string(eg. fNIRS) upon being given the name of an all data file
#The format should be SENSOR_SUBJECTNUMBER.csv
def getDataType(name):
    data_type = ""
    for ch in name:
        if(ch == '_'):
            return data_type
        data_type += ch

#Given a list of Files, it groups the files into their subjects.
#The file format should be SENSOR_SUBJECTNUMBER.csv
def groupSubjects(Files):
    Subjects = []
    while Files:
        print("LOOP")
        subject = []
        cur = getSubjectNumber(Files[0])
        for item in Files:
            if getSubjectNumber(item) == cur:
                subject.append(item)
        for item in subject:
            Files.remove(item)
        Subjects.append(subject)
    return Subjects
            
            
#==========================FILE CONCATENATION===================================

#Concatenate takes Arff Files and combines them
def concatenate(num_subjects, Subjects, length, name):
    all_data= []
    for i in range(num_subjects):
        cur = []
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
        cur = []
        with open(Data[i]) as f:
            for line in f:
                cur.append(line)
        for z in range(arffLine[getDataType(Data[i])] * numChans[getDataType(Data[i])] + 3):
            cur.pop(0)
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

#===============================================================================
#===========================RUNNING EVERYTHING==================================
#===============================================================================

#Server_URL paramater edited out
def run(subject,num_k,n_num,conditions,zscore,roi,ext):

    print("STARTED RUNNING")

    #Dictionary for the number of channels in each data type
    numChans = {}

    #Gets the number of chans for each data type in this subject
    for data_name in subject:
        print(subject)
        data = open_csv(data_name)
        datatype = getDataType(data_name)
        if datatype.upper() == "FNIRS":
            print(len(data[0]))
            numChans[datatype] = len(data[0])/2
        elif datatype.upper() == "EEG":
            numChans[datatype] = len(data[0])/9

    #Runs for each individual file
    for data_name in subject:
        datatype = getDataType(data_name)
        head = getSubjectNumber(data_name)
        conds_name = datatype + '_' + head +'_conditions.csv' #EDITED FROM head + '_conditions_valence'
    
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
        if zscore:
            if datatype.upper() == 'FNIRS':
                for j in range(num_chans*2):
                    zary = []
                    for i in range(len(data)-2):
                        zary.append(data[i+2][j])
                    zary = stats.zscore(zary)
                    for i in range(len(data)-2):
                        data[i+2][j] = zary[i]

            elif datatype.upper() == 'EEG':
                for j in range(num_chans*9):
                    zary = []
                    for i in range(len(data)-9):
                        zary.append(data[i+9][j])
                    zary = stats.zscore(zary)
                    for i in range(len(data)-9):
                        data[i+9][j] = zary[i]

    #=======================REGION OF INTEREST ANALYSIS=============================

        # NOTE: This section is optional, might not be used every time
        if roi and datatype == "fNIRS":
            # Reading the ROI lines from a file
            ROI_lines = []
            #with open('ROI_'+head+'.txt','rb') as f:
            with open('ROI_file_2000s.txt','rb') as f:
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
        write_sep_data(data,num_chans,datatype +'_' + head,datatype)
        marks = [['start','end','condition']]
        for i in range(num_conds+1):
            if i == 0 or conditions.find(str(i)) == -1:
                continue
            for j in range(len(conds[i*2])-2):
                row = [str(conds[i*2-1][j+2]),
                       str(conds[i*2-1][j+2]+conds[i*2][j+2]),
                       str(i)]
                marks.append(row)
        
        # formats the conditions file into a [starts,ends, condition] file to
        # be used in the arff file generator
        write_csv(datatype + '_' + head +'_Marks.csv',marks)

        print("CONVERTED TO MARKS FILE")

#========================PASSING TO ARFFGEN====================================       

        # arff file generator passed in, pass 1 into subjects until further notice
        arff_generate(datatype + '_' + head,num_conds,1,num_chans,conditions)

        print("PASSED TO ARFF GEN")

#=============================PASSING IN ORANGE=================================

    
    print("PASSING TO ORANGE")

    #Creates an array of arff files for each sensor in the subject to be fused
    Arffs = []
    for item in subject:
        name = getDataType(item) + "_" + getSubjectNumber(item) + "_Arff.arff"
        Arffs.append(name)

    #combineDataTypes returns the # of attributes
    length = combineDataTypes(Arffs, numChans)
    
    write_csv((head+'_ML_Data'+ext),orange("fuse_" + head + "_Arff.arff",num_k,n_num))
    
    return length

    print("PASSED TO ORANGE")

#===============================================================================
#=================================MAIN==========================================
#===============================================================================


def main():
#==============================USER INPUTS======================================

#-------------------------------------------------------------------------------
    # WHOEVER IS USING THIS PROGRAM SHOULD CHANGE THESE TO WHATEVER THEY LIKE
    # SAX INPUTS
    # JUST REPLACE THE NUMBERS, DONT TOUCH THE COMMENT AFTER ESPECIALLY THE #
    word = 4 # word length for each channel
    letter = 5 # alphabet size, has to be greater than 3. less than 20

    # FILE INPUTS 
    # JUST ENTER THE STARTING NUMBER OF THE EXPERIMENT AND THE NUMBER OF
    # FILES
    Files = ['EEG_2004.csv', 'fNIRS_2004.csv','EEG_2002.csv', 'fNIRS_2002.csv']
    #starter = '2'
    #p_start = 15
    #p_end = 16
    num_files = len(Files) # (p_end - p_start) + 1
    
    # EDITED OUT: TO OMIT
    # EDITED OUT: Server URL

    # Z-SCORE, NORMALIZING THE DATA
    # TYPE 'False' IF YOU DONT WANT IT, 'True' IF YOU DO
    zscore = False

    # REGION OF ANALYSIS
    roi = True

    # LIST THE CONDITIONS NUMBERS WITHOUT ANY SPACES IN BETWEEN EACH ONE
    conditions = "12" # Which conditions do we want to look at for each file
    # FILE EXTENSION
    # Change each time you run to reflect where you would like the results to
    # be written to, MAKE SURE IT ALWAYS ENDS IN '.CSV
    ext = '_1v2_roi_yes.csv' 
    
    # ORANGE INPUTS
    # K-NEAREST NEIGHBOR
    num_k = 10  # how many neighbors
    n_num = 100  # feature selection importance
#-------------------------------------------------------------------------------
    Subjects = groupSubjects(Files)

    # Running the single files
    for item in Subjects:
       heads=run(item,num_k,n_num,conditions,zscore,roi,ext)
    
    #Running the single concatenated file
    concatenate(len(Subjects),Subjects,3828,"All_Test_Data.arff") #3828 replace with heads
    
    print("Still Running 2")
    
    #Writing ML Data for concatenated files
    name = 'All_Test_Data'  #--Maybe change this to read 'All_extension_data
    write_csv((name+'_ML_Data'+ext),orange(name,num_k,n_num))

    print("Still Running 3")
    # Running the Leaving a file out concatenated files
    for i in range(len(Subjects)):#Edited Loop   #--Again make it run through Files
        left = []
        for z in range(len(Subjects)):
            if z != i:
                left.append(Subjects[z])
        concatenate(len(Subjects) - 1, Left, heads, "second")
        write_csv(name+'_ML_Data'+ext,
                  orange_two('T'+'{0:0>3}'.format(str(i)),num_k,
                             n_num))
              
#===============================================================================
#==============================CLOSE MAIN=======================================
#===============================================================================

main()
