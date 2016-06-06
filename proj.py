################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2015                        #
#                  Russell Glick '17 and Ben Sklar '18                         #
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

#=========================SEPARATING OXY / DEOXY================================

def write_sep_data(data,chans,name):
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

#==========================FILE CONCATENATION===================================

def concatenate(num_files,starter,end,length,left,pstart):
    #end is '000_Data_Sax...' part
    all_data= []
    for i in range(pstart,num_files+1):
        if i == left:
            continue
        head = starter + '{0:0>3}'.format(str(i))
        cur = []
        with open((head+'_All_Data_'+end),'rb') as f:
            for line in f:
                cur.append(line)
        if (left != pstart and i != pstart) or (left == pstart and i != (pstart+1)):
            for j in range(length):
                cur.pop(0)
        all_data += cur
    
    name = 'All_'+starter+'000_Data_'
    if left != 0:
        name += ('No_'+starter+'{0:0>3}'.format(str(left))+'_')
    
    with open((name+end),'wb') as f:
        for i in range(len(all_data)):
            f.writelines(all_data[i])

#==========================SAX REPRESENTATION===================================

def sax_rep(word,letter,ary):
    ary = np.asarray(ary)
    sax = SAX(word,letter)
    return sax.to_letter_rep(ary)

#===============================================================================
#===========================RUNNING EVERYTHING==================================
#===============================================================================

def run(head,word,letter,num_k,n_num,conditions,zscore,roi,ext):

    data_name = head + '_All_Data'
    conds_name = 'condition_' + head  
    
#==========================INPUTTING DATA FILES=================================
    
    # open files
    data = open_csv(data_name+'.csv')
    conds = open_csv(conds_name+'.csv')
    num_chans = len(data[0])/2
    # separates total data into separate oxy and deoxy files, to be used
    # in the arff file generator and then Orange
    data = data_format(data,num_chans)
    conds = cond_format(conds)
    num_conds = (len(conds)-1)/2

#===========================Z-SCORING THE DATA==================================

    # NOTE: This section is optional, might not be used every time
    if zscore:
        for j in range(num_chans*2):
            zary = []
            for i in range(len(data)-2):
                zary.append(data[i+2][j])
            zary = stats.zscore(zary)
            for i in range(len(data)-2):
                data[i+2][j] = zary[i]

#=======================REGION OF INTEREST ANALYSIS=============================

    # NOTE: This section is optional, might not be used every time
    if roi:
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

#========================CONVERTING TO MARKS FILE===============================
    
    # Separate the oxy and deoxy data for the arff file generator
    write_sep_data(data,num_chans,data_name)
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
    write_csv(data_name+'_Marks.csv',marks)
    
#========================SAX/SUMMER '12 REPRESENTATIONS=========================
    
    # Creating the Sax Representation (Writing it to a file)
    sax_lines = []
    sax = ""
    for i in range(num_conds+1):
        # Checking which data we need by condition,
        if i == 0 or conditions.find(str(i)) == -1:
            continue
        for j in range(len(conds[i*2])-2):
            start = conds[i*2-1][j+2]
            run = conds[i*2][j+2]
            for k in range(num_chans*2): # getting every channel
                ary = []
                for m in range(run):
                    ary.append(data[start+m][k])
                sax += sax_rep(word,letter,ary)[0]
            
            newsax = ""
            for n in range(len(sax)):
                newsax += (str((ord(str(sax[n]))-96))+"\t")
            
            # adding the header lines to the output file
            if sax_lines == []:
                first_line = ""
                second_line = ""
                for f in range(num_chans*2):
                    for g in range(word):
                        first_line += ("Ch" + str((f%num_chans)+1))
                        if f < num_chans:
                            first_line += "Oxy"
                        else:
                            first_line += "Deoxy"
                        first_line += ("Pos"+str(g+1)+"\t")
                        second_line += "d\t"
                first_line += "condition\n"
                second_line += "d\n"
                sax_lines.append(first_line)
                sax_lines.append(second_line)
                sax_lines.append((num_chans*word*2) * "\t" + "class\n")
            newsax += (str(i)+"\n")
            sax_lines.append(newsax)
            sax = ""
    
    # Writing the SAX lines to a file
    with open((data_name+'_Sax_Output.tab'),'wb') as f:
        for i in range(len(sax_lines)):
            f.writelines(sax_lines[i])
    
    # arff file generator passed in, pass 1 into subjects until further notice
    arff_generate(data_name,num_conds,1,num_chans,conditions)

#=============================PASSING IN ORANGE=================================

    write_csv((head+'_ML_Data'+ext),orange(data_name,num_k,n_num))
    return (66*num_chans+3)

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
    starter = '2'
    pstart = 2
    num_files = 19

    # Z-SCORE, NORMALIZING THE DATA
    # TYPE 'False' IF YOU DONT WANT IT, 'True' IF YOU DO
    zscore = False

    # REGION OF ANALYSIS
    roi = True

    # LIST THE CONDITIONS NUMBERS WITHOUT ANY SPACES IN BETWEEN EACH ONE
    conditions = "123" # Which conditions do we want to look at for each file
    # FILE EXTENSION
    # Change each time you run to reflect where you would like the results to
    # be written to, MAKE SURE IT ALWAYS ENDS IN '.CSV
    ext = '1v2v3_O_E_ROI.csv' 
    
    # ORANGE INPUTS
    # K-NEAREST NEIGHBOR
    num_k = 10  # how many neighbors
    n_num = 100  # feature selection importance
#-------------------------------------------------------------------------------
    
    # Running the single files
    for i in range(pstart,num_files + 1):
        heads=run(starter + '{0:0>3}'.format(str(i)),word,letter,num_k,n_num,
                  conditions,zscore,roi,ext)
    
    # Running the single concatenated file
    concatenate(num_files,starter,'Sax_Output.tab',3,0,pstart)
    concatenate(num_files,starter,'Arff.arff',heads,0,pstart)
    # Writing ML Data for concatenated files
    name = 'All_'+starter+'000_Data'
    write_csv((name+'_ML_Data'+ext),orange(name,num_k,n_num))

    # Running the Leaving a file out concatenated files
    for i in range(pstart,num_files+1):
        concatenate(num_files,starter,'Sax_Output.tab',3,i,pstart)
        concatenate(num_files,starter,'Arff.arff',heads,i,pstart)
        write_csv(name+'_ML_Data_No'+starter+'{0:0>3}'.format(str(i))+ext,
                  orange_two(starter,starter+'{0:0>3}'.format(str(i)),num_k,
                             n_num))
              
#===============================================================================
#==============================CLOSE MAIN=======================================
#===============================================================================

main()
