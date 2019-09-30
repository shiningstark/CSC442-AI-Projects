# read the data file and parser
def readfile(filename):
    file = open(filename)
    str = file.readlines()
    res = [s.strip().split(',') for s in str]
    return res
