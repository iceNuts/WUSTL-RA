# -*- coding: utf-8 -*-

#created by Li Zeng on May/10/2013
import os
import sys
import threading
import time
import re
import codecs

#main
def main(argv):
    #support functions
    import getopt
    def usage():
        print ('usage: %s [-p target foder path]' % argv[0])
        return 100
    def programTerminate():
        return 101    
        
    try:
        (opts, args) = getopt.getopt(argv[1:], 'p:d:')
    except getopt.GetoptError:
        return usage()
    #check if parameter number exceeds
    if args: return usage()
    #get path parameters
    (params, targetPath) = opts[0]
    
    #read files in targetPath
    try:
        dirList = os.listdir(targetPath)
    except os.error:
        print ('target folder is invalid')
        return programTerminate()
  
    #thread control parameters
    threadCount = 0
    threadLimit = 8
    threadIdleTime = 5 #seconds
    
    for entry in dirList:
        #Avoid Huge Consumption
        if threadCount == threadLimit:
            time.sleep(threadIdleTime)
            threadCount = 0
        
        entryPath = os.path.join(targetPath, entry)
        entryName = os.path.splitext(entry)[0]
        extension = os.path.splitext(entry)[1]
        
        if not extension or extension != '.txt': continue
        #run thread 
        worker = cleantxtWorker(entryPath)
        #thread start
        try:
            worker.start()
            threadCount += 1
        except RuntimeError:
            print ('thread invokation error - internal crack')
            return programTerminate()
    
    return 0
    
class cleantxtWorker(threading.Thread):
    def __init__(self, entryPath):
        threading.Thread.__init__(self)
        self.entry = entryPath

    def run(self):
        new_file = ""

        with open(self.entry) as input_file:
            lines = input_file.readlines()
            for line in lines:
                if line:
                    new_file += (line.rstrip() + " ")
        input_file.close()

        with open(self.entry, 'w') as output_file:
            new_file = self.clean_Spanish_letters(new_file)
            output_file.write(new_file)
        output_file.close()
        
    def clean_Spanish_letters(self, input_text):
        'clean Spanish text -- re.match and re.search often dont work with some characters'
        input_text = re.sub('á', 'a', input_text)
        input_text = re.sub('Á', 'A', input_text)
        input_text = re.sub('é', 'e', input_text)
        input_text = re.sub('É', 'E', input_text)
        input_text = re.sub('í', 'i', input_text)
        input_text = re.sub('í', 'I', input_text)
        input_text = re.sub('Ó', 'O', input_text)
        input_text = re.sub('ó', 'o', input_text)
        input_text = re.sub('ú', 'u', input_text)
        input_text = re.sub('Ú', 'U', input_text)
        input_text = re.sub('ñ', 'n', input_text)
        input_text = re.sub('Ñ', 'N', input_text)
        return input_text

if __name__ == '__main__': sys.exit(main(sys.argv))



