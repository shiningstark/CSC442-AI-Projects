import  xml.dom.minidom
import re
import os
class Node:     # every node in bayes net
    def __init__(self):
        self.variablename = ""
        self.given = ""
        self.condpro = []
        self.parents = []
        self.children = []


class Db:       # bayes net
    def __init__(self):
        self.variables = {}
        self.nodetree = []      # store the node of every variable

    def parser(self,filepath):      # as the filepath to get data
        dom = xml.dom.minidom.parse(os.getcwd()+"\\examples\\"+filepath)
        # dom = xml.dom.minidom.parse(os.getcwd()+"\\examples\\"+"dog-problem.xml")
        root = dom.documentElement
        variables = root.getElementsByTagName("NAME")       # get variable name from document
        for i in range(1,len(variables)):
            if variables[i].childNodes[0].data not in self.variables:
                self.variables[variables[i].childNodes[0].data] = []
        probabilities = root.getElementsByTagName("DEFINITION")     # some document have that, some don't
        for probability in probabilities:
            query = probability.getElementsByTagName("FOR")[0].childNodes[0].data
            conditions = probability.getElementsByTagName("GIVEN")
            evidences = probability.getElementsByTagName("TABLE")[0].childNodes
            sentence1 = ""
            if conditions:      # as given set the value of variables
                for i in range(len(conditions)):
                    sentence1 = sentence1 + conditions[i].childNodes[0].data + "|"
                if sentence1.count("|") == 1:
                    sentence2 = ["0","1"]
                else:
                    sentence2 = ["00","01","10","11"]
            else:
                sentence2 = ["0","1"]
            pro = []
            if sentence1.count("|") < 1:        # if the variable is root
                a = re.split (r'[\s\s]', evidences[ 0 ].data)
                a = [ x for x in a if x != "" ]
                pro.append(a)
            else:
                if root.getElementsByTagName ("PROPERTY"):      # if the table is different format
                    a = re.split (r'[\s\s]', evidences[ 0 ].data)
                    a = [ x for x in a if x != "" ]
                    for j in range(len(a)-1):
                        if j%2 ==0:
                            b = [a[j],a[j+1]]
                            pro.append(b)
                else:
                    for j in range (2, len (evidences)):
                        if j % 2 == 0:
                            evidences[ j ].data = evidences[ j ].data.replace ("\n\t", "")
                            a = evidences[ j ].data.strip ()
                            a = re.split (r'[\s\s]', a)
                            a = [ x for x in a if x != "" ]
                            # print(a)
                            if len (a) > 1:
                                pro.append (a)
            self.variables[query].append([sentence1])       # build the probability of bayes net
            self.variables[query].append(sentence2)
            self.variables[query].append(pro)
        # print(self.variables.keys())


    def createDAG(self):        # create the DAG tree
        for key,value in self.variables.items():
            treenode = Node()
            treenode.variablename = key
            treenode.given = value[0]
            treenode.condpro = value[1:]
            self.nodetree.append(treenode)
        for i in self.nodetree:
            if self.variables[i.variablename][0][0] != "":
                var = self.variables[i.variablename][0][0].split("|")
                var = [x for x in var if x != ""]
                for j in var:
                    for l in self.nodetree:
                        if l.variablename == j:
                            i.parents.append(l)
                            l.children.append(i)
        tempvariable = {}
        for i in self.nodetree:
            if i.parents == []:
                tempvariable[i.variablename] = self.variables[i.variablename]
        flag = len(tempvariable.keys())
        while(flag <len(self.variables.keys())):
            for i in self.nodetree:
                for j in i.children:
                    if i.variablename in tempvariable and j.variablename not in tempvariable:
                        tempvariable[j.variablename] = self.variables[j.variablename]
                        flag += 1
        self.variables = tempvariable
        print (self.variables)