from math import log
class Node:
    def __init__(self,attribute,parent):
        self.attributeset = None
        self.parent = parent
        self.attribute = attribute
        self.value = None
        self.next = []
        self.output = None
class DT:
    def __init__(self,examples):
        self.examples = examples
        self.size = len(examples)
        self.attribute = list(range(len(examples[0])-1))

    # extract date from data file
    def createDatebase(self,examples):
        self.values = {}
        for i in range(len(examples[0])):
            if i not in self.values:
                self.values[i] = []
            for j in range(len(examples)):
                if examples[j][i] not in self.values[i]:
                    self.values[i].append(examples[j][i])

    # using entropy function to rank all attributes
    def rank(self):
        self.importance = []
        lable = self.values[len(self.examples[0])-1]
        for i in range(len(self.examples[0])-1):
            dic = {}
            res = 0
            instance = [0] * len(self.values[len(self.examples[0])-1])
            B = 0
            for j in range(len(self.examples)):
                if self.examples[j][i] not in dic:
                    dic[self.examples[j][i]] = [0] * (len(self.values[len(self.examples[0])-1])+1)
                dic[ self.examples[ j ][ i ] ][-1] += 1
                for l in range(len(lable)):
                    if self.examples[j][-1] == lable[l]:
                        dic[ self.examples[ j ][ i ] ][ l ] += 1
            for total,positive in dic.items():
                for j in range(len(positive)-1):
                    res += (positive[-1] / self.size) * self.calH(positive[j],positive[-1])
                    instance[j] += positive[j]
            for j in range(len(instance)):
                B += self.calH(instance[j],self.size)
            gain = B - res
            self.importance.append(gain)

    # simplify the mathematic function
    def calH(self,positive,total):
        q = float(positive / total)
        if q != 1 and q != 0:
            return float(-(q * log(q,2)))
        else:
            return float(0)
    def remain(self,value,attr,dataset):
        if dataset:
            newdataset = []
            for i in range(len(dataset)):
                if dataset[i][attr] == value:
                    newdataset.append(dataset[i])
            return newdataset
        return []

    # when there is no attributes or examples, assign the label based on remaining data
    def plurality_value(self,examples):
        num = [0] * len(self.values[len(self.examples[0])-1])
        for i in examples:
            for j in range(len(self.values[len(self.examples[0])-1])):
                if i[-1] == self.values[len(self.examples[0])-1][j]:
                    num[j] += 1
        index = num.index(max(num))
        return self.values[len(self.examples[0])-1][index]

    # assign label when dataset can be classified as same class
    def classification(self,examples):
        count = [0] * len(self.values[len(self.examples[0])-1])
        for i in examples:
            for j in range(len(self.values[len(self.examples[0])-1])):
                if i[-1] == self.values[len(self.examples[0])-1][j]:
                    count[j] += 1
        for i in count:
            if i == len(examples):
                return examples[0][-1]
        return -1

    # choose the best attribute
    def selectAttr(self,attributes):
        temp = []
        largest = 0
        for i in attributes:
            temp.append(self.importance[i])
            if self.importance[i] > largest:
                largest = self.importance[i]
        for j in range(len(self.importance)):
            if self.importance[j] == largest and j in attributes:
                return j

    # create the whole decision tree
    def creatTree(self,examples,attributes,value,parents_examples,node):
        if len(attributes) == 0:
            node.output = self.plurality_value(examples)
            return
        elif not examples:
            attr = self.selectAttr (attributes)
            leaf = Node (attr,node.attribute)
            leaf.value = value
            leaf.output = self.plurality_value(parents_examples)
            return leaf
        elif self.classification(examples) != -1:
            flag = self.classification(examples)
            attr = self.selectAttr(attributes)
            leaf = Node(attr,node.attribute)
            temp = attributes[:]
            temp.remove (attr)
            leaf.attributeset =temp
            leaf.value = value
            leaf.output = flag
            return leaf
        else:
            attr = self.selectAttr(attributes)
            root = Node(attr,node.attribute)
            temp = attributes[:]
            temp.remove(attr)
            root.attributeset = temp
            root.value = value
            for i in range(len(self.values[attr])):
                remain = self.remain(self.values[attr][i],attr,examples)
                subtree = self.creatTree(remain,root.attributeset,self.values[attr][i],examples,root)
                if subtree:
                    root.next.append(subtree)
        return root

    # use testdate for test
    def test(self,testdata,tree):
        right = 0
        for j in testdata:
            right += self.checktree(j,tree)
        return float(right/len(testdata))

    # check the result as the decision tree
    def checktree(self,example,tree):
        if not tree.next:
            if example[tree.parent] == tree.value and example[-1] == tree.output:
                return 1
            else:
                return 0
        else:
            for i in tree.next:
                if example[tree.attribute] == i.value:
                    return self.checktree(example,i)