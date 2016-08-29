from scipy.io.arff import loadarff
import scipy as sp
import os
import csv

def convert(arff_file):
	rel_path = arff_file + '.arff' # File being converted
	rel_path_csv = arff_file + '.tab' # Name of new file
	abs_file_path = os.path.join(rel_path)
	dataset = loadarff(open(abs_file_path,'r'))

	abs_file_path_csv = os.path.join(rel_path_csv)
	f=open(abs_file_path_csv, 'wb');
	writer = csv.writer(f, delimiter='\t') 

	# Write attribute header
	for i in dataset[1]:
	    f.write(i)
	    f.write('\t')
	f.write('\n')

	# Write datatype header
	for i in dataset[1]:
	    if i== 'condition':
	        f.write('d')
	    else:
	        f.write('c')
	    f.write('\t')
	f.write('\n')

	# Write class header
	for i in dataset[1]:
	    f.write('\t')
	f.write('class')
	f.write('\n')

	# Addition by Eseosa Asiruwa
	# Get the rest of the data information
	# Store them in rows
	data_rows = []
	for i in range(len(dataset[0])):
		data_rows.append(dataset[0][i])

	# Write the rows to the file
	writer.writerows(data_rows)

	f.close()
