from Parser import readfile
from Tree import *
import random

# k cross-validation
def validation(dataset,k):
    start = 0
    end = k
    right = []
    for i in range(int(len(dataset)/k)):        # split the dataset
        testdata = list(dataset[j] for j in range(start,end))
        traindata = list(l for l in dataset if l not in testdata)
        decisiontree = DT (traindata)
        decisiontree.createDatebase(sample)
        decisiontree.rank()
        print(decisiontree.importance)
        tree = decisiontree.creatTree (traindata, decisiontree.attribute, None, None,Node(None,None))      #create decision tree
        right.append(decisiontree.test(testdata,tree))      # using testdate for test performace of the tree
        start += k
        end += k
        if end > len(dataset):
            end = len(dataset)
    # print(sum(right)/len(right))

def randomorder(dataset,index):
    # for i in range(len(dataset)):
    #     classattr = dataset[i][index]
    #     dataset[i].remove(classattr)
    #     dataset[i].append(classattr)
    return random.sample(dataset,len(dataset))      # randomly distribute the dataset

# main entrance for the program
if __name__ == '__main__':
    sample = readfile("./data/iris.data.discrete.txt")
    sample = randomorder (sample, 0)
    for i in range(1,80):
        validation(sample,i)
    # validation (sample, 1)