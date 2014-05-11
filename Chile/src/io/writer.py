import os
import sys
import csv

def write_csv(destpath, filename, content):
    if not os.path.exists(destpath):   os.makedirs(destpath)        
    with open(os.path.join(destpath, filename), 'a') as input_file:
        writer = csv.writer(input_file, delimiter=',')
        writer.writerows(content)
    input_file.close()
