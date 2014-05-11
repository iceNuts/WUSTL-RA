#created by Li Zeng on Oct/21/2013
import os
import sys
import threading
import time

#main
def main(argv):
    #support functions
    import getopt
    def usage():
        print ('usage: %s [-p target foder path] [-d destination folder path]' % argv[0])
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
    (params, destPath)   = opts[1]
    
    #read files in targetPath
    try:
        dirList = os.listdir(targetPath)
    except os.error:
        print ('target folder is invalid')
        return programTerminate()
        
    #create dest path folder
    if not os.path.exists(destPath):   os.makedirs(destPath)
    
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
        
        if not extension or extension != '.pdf': continue
        outputPath = os.path.join(destPath, entryName)
        #run thread 
        worker = pdf2txtWorker(entryPath, outputPath)
        #thread start
        try:
            worker.start()
            threadCount += 1
        except RuntimeError:
            print ('thread invokation error - internal crack')
            return programTerminate()
    
    return 0
    
class pdf2txtWorker(threading.Thread):
    def __init__(self, targetPath, destPath):
        threading.Thread.__init__(self)
        self.target = targetPath
        self.dest   = destPath
    def run(self):
        #command = "python scripts/pdf2txt.py -o " + self.dest + " " + self.target
        command = "pdftotext -nopgbrk -cfg ~/.xpdfrc " + self.target + " " + self.dest + ".txt"
        ret = os.system(command)
    
if __name__ == '__main__': sys.exit(main(sys.argv))










    