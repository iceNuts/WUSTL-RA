import field
import os
import sys
import io



def main(argv):
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
    (params, targetpath) = opts[0]
    (params, destpath)   = opts[1]

    dirlist = io.reader.read_dir(targetpath)    

    header = [['FILENAME', 'LEGISLATURE_NUMBER', 'LEGISLATURE_TYPE', 'SESSION_NUMBER', 'DATE']]

    io.writer.write_csv(destpath, "SESSION_INFO.csv", header)

    for entry in dirlist:
        entrypath = os.path.join(targetpath, entry) 
        lines = io.reader.read_file(entrypath)

        if lines:
            data = [
                        [
                            entry,
                            field.legislaturenumber.fetch(lines[0]),
                            field.legislaturetype.fetch(lines[0]),
                            field.sessionnumber.fetch(lines[0]),
                            field.date.fetch(lines[0])
                        ]
                    ]
            try:
                io.writer.write_csv(destpath, "SESSION_INFO.csv", data)
            except Exception, e:
                print ("file %s write failed", entry)

    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))









