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

# get formating from proj.py

#===========================SEPERATING DATA=====================================

def write_sep_data(data, chans, name):
    # Timestamps
    epoch = []

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

    # Save timestamps in array 
    

    # Iterate through provided data, row by row, put row data into correct array
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
                if k == 1:
                    tslow_row.append(data[i][(9 * j) + k])
                elif k == 2:
                    tfast_row.append(data[i][(9 * j) + k])
                elif k == 3:
                    ttotal_row.append(data[i][(9 * j) + k])
                elif k == 4:
                    afast_row.append(data[i][(9 * j) + k])
                elif k == 5:
                    aslow_row.append(data[i][(9 * j) + k])
                elif k == 6:
                    atotal_row.append(data[i][(9 * j) + k])
                elif k == 7:
                    beta_row.append(data[i][(9 * j) + k])
                elif k == 8:
                    gamma_row.append(data[i][(9 * j) + k])
                elif k == 9:
                    sigma_row.append(data[i][(9 * j) + k])

        theta_slow.append(tslow_row)
        theta_fast.append(tfast_row)
        theta_total.append(ttotal_row)
        alpha_slow.append(aslow_row)
        alpha_fast.append(afast_row)
        alpha_total.append(atotal_row)
        beta.append(beta_row)
        gamma.append(gamma_row)
        sigma.append(sigma_row)

   # for i in range(len(theta_slow)):
            #print(theta_slow[i])
    for i in range(len(epoch)):
        print(epoch[i])

    write_csv(name+'_ThetaSlow.csv',theta_slow)
    write_csv(name+'_ThetaFast.csv',theta_fast)
    write_csv(name+'_ThetaTotal.csv',theta_total)
    write_csv(name+'_AlphaSlow.csv',alpha_slow)
    write_csv(name+'_AlphaFast.csv',alpha_fast)
    write_csv(name+'_AlphaTotal.csv',alpha_total)
    write_csv(name+'Beta.csv',beta)
    write_csv(name+'Gamma.csv',gamma)
    write_csv(name+'Sigma.csv',sigma)


#===============================================================================
#=================================MAIN==========================================
#===============================================================================

def main():
    # Open data files
    #data = open_csv('test.csv')
    data = open_csv('SubjectID_All_Data_EEG.csv')

    # Number of channels is the length of the data arrays
    # divided by 9 because there are 9 individual EEG data
    # categories per channel
    num_chans = len(data[0])/9

    data_name = 'temp'

    # Separate data
    write_sep_data(data, num_chans, data_name)

    # Print out all data in array
    # for i in range(len(data)):
    #         print(data[i])



#===============================================================================
#==============================CLOSE MAIN=======================================
#===============================================================================

main()
