import os
import sys


def read_dir(path):
    try:
        dirList = os.listdir(path)
    except os.error:
        print ('target folder is invalid')
        exit(0)

    #remove .DS_Store file if exist
    try:
        dirList.remove(".DS_Store");
    except ValueError:
        pass

    dirList.sort(key=lambda x: int(x[len("ChilDep2001n") - len(x): -4]))

    return dirList

def read_file(path):
    try:
        with open(path) as inputFile:
            lines = (line.rstrip() for line in inputFile)
            lines = list(line for line in lines if line)
        inputFile.close()
        return lines
    except Exception, e:
        print ('read file %s failed', path)
        return None
        
