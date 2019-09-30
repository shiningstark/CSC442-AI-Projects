import re

class dpll_tree:    # it is the dpll tree structure
    def __init__(self,bool,unprove,parent = None):
        self.left,self.right = None,None    # child node
        self.parent = parent        # parent node
        self.bool = bool            # the value represent the truth or false
        self.flag = 0               # check if it is done
        self.unprove = unprove      # the rest clauses unproved after assignments


class KB:               # knowledge base structure
    def __init__(self):
        self.kb = []    # initial sentence
        self.table = [] # all the variables
        self.model = [] # all the model
    def tell(self,sentence):
        # element = self.parser(sentence)
        # self.kb.append(element)
        # self.revised()
        clause,items = self.parser(sentence)    # use parser function to split the sentence
        for i in clause:
            if i not in self.kb:
                self.kb.append(i)               # all the clause in kb(the clause will contain the negation)
        for i in items:
            if i not in self.table:
                self.table.append(i)            # pure variables into table
        self.temp = self.kb[:]
    def ask(self,sentence):
        # self.tell(sentence)
        tree = self.createtree(0,self.kb,str(0),None,1) # create the dpll tree and use variable tree to debug even though it's not used


    def findclaues(self,var,value,unprove):
        proveclaues = []
        for k in unprove:
            variable = re.split(r'[\|]', k)
            variable = [x for x in variable if x !='']
            if value ==1:
                for l in variable:
                    if var in l and "-" not in l :
                        proveclaues.append(k)
            else:
                for l in variable:
                    if var in l and "-" in l :
                        proveclaues.append(k)
        return proveclaues

    def createtree(self,index,temp,var,parent,number): # create tree, index represent the place of variable in table,
                                                       # temp means unproved clauses, var means the value of variable including all assignments
                                                       # parents is parent node, number represent what assignment of node
        if index == 0: # create the root node
            node = dpll_tree("",self.kb)    # root node is no value and unproved clauses is whole knowledge base
            node.left = self.createtree(index+1, node.unprove, "", node,0)  # all the left node is assigned false
            node.right = self.createtree(index+1, node.unprove, "", node,1) # all the left node is assigned truth
        elif index>len(self.table): # if all variables have assignment, it ends
            return None
        else:
            a = self.findclaues(self.table[index-1],number,temp)    # use find clause to get proved clauses
            copy = temp[:]
            for j in a:
                if j in copy:
                    copy.remove(j)   # temp is unproved clauses, so after assigning, remove the proved clauses from temp
            node = dpll_tree(var+str(number),copy,parent)   #create node
            if len(node.unprove) == 0:  # if every clause have been proved, it ends
                node.flag = 1
                self.model.append(node.bool)
                return node
            elif index <len(self.table):    # when it dose not end, continue to create tree
                node.left = self.createtree(index+1,node.unprove,node.bool,node,0)
                node.right = self.createtree(index+1,node.unprove,node.bool,node,1)
            else:   # all assignments have done, it ends
                return node
        return node


    # def ask(self,sentence):
    #     # self.tell(sentence)
    #     a = 2**len(self.table)-1
    #     result = a+1
    #     while(a>=0):
    #         b = list(bin(a)[2:])
    #         while len(b)<len(bin(2**len(self.table)-1)[2:]):
    #             b.insert(0,"0")
    #         if self.check(b) == 0:
    #             str = re.split(r'[\(\)\|]',sentence)
    #             str = [x for x in str if x != ""]
    #             count = len(str)
    #             for j in str:
    #                 c = re.split(r'[\-]', j)
    #                 c = [x for x in c if x != ""]
    #                 if b[self.table.index(c[0])] == "0" and "-" not in j:
    #                     count -= 1
    #                 elif b[self.table.index(c[0])] == "1" and "-" in j:
    #                     count -= 1
    #                 if count == 0:
    #                     if sentence in "abcdefgh":
    #                         print(sentence+" is knave!!")
    #                     else:
    #                         print(sentence + " is bad door!!")
    #                     return
    #         else:
    #             result -= 1
    #         a -= 1
    #     if result == 0:
    #         # self.delete()
    #         print("no conclusion!!")
    #     else:
    #         if sentence in "abcdefgh":
    #             print(sentence + " is knight!!")
    #         else:
    #             print(sentence + " is good door!!")

    # def delete(self):
    #     self.kb.pop()

    def parser(self,sentence):  # Though input sentences have been CNF, but still split base on every possible signs
         # a = re.split(r'([\-\^\&\(\)\>\=])', sentence)
         a = re.split(r'[\&]', sentence)
         b = re.split(r'[\-\|\&\(\)\>\=]', sentence)
         return [x for x in a if x!=''],[x for x in b if x!='']

    # def check(self,a):
    #     for i in self.kb:
    #         b = re.split(r'[\(\)\|]',i)
    #         b = [x for x in b if x !=""]
    #         count = len(b)
    #         for j in b:
    #             c = re.split(r'[\-]',j)
    #             c = [x for x in c if x != ""]
    #             if a[self.table.index(c[0])] == "0" and "-" not in j:
    #                 count -= 1
    #             elif a[self.table.index(c[0])] == "1" and "-" in j:
    #                 count -= 1
    #             if count == 0:
    #                 return 1
    #     return 0
    # def revised(self):
    #     for i in range(len(self.kb)):
    #         self.revised_equal()
    #         self.revised_entailment()
    #         sentence = self.kb[i][:]
    #         sentence = self.revised_negotion(sentence)
    #         # print(sentence)
    #         sentence = self.revised_dbneg(sentence)
    #         # print(sentence)
    #         sentence = self.revised_dbbrackets(sentence)
    #         print(sentence)
    #         sentence = self.CNF(sentence)
    #         # sentence = self.revised_dbbrackets(sentence)
    #         self.kb[i] = sentence[:]
    #         print(self.kb[i])
    #     # for i in range(len(self.kb)):
    #     #     str =""
    #     #     for j in self.kb[i]:
    #     #         str += j
    #     #     self.kb[i] = str
    #
    # def revised_equal(self):
    #     for i in range(len(self.kb)):
    #         for j in range(len(self.kb[i])-1):
    #             if self.kb[i][j] == "=":
    #                 a = ["("] + self.kb[i][:j-1] + [">"] + self.kb[i][j+1:] + [")"]
    #                 b = ["("] + self.kb[i][j+1:] + [">"] + self.kb[i][:j-1] + [")"]
    #                 self.kb.remove(i)
    #                 self.kb.append(a)
    #                 self.kb.append(b)
    #
    # def revised_entailment(self):
    #     for i in range(len(self.kb)):
    #         for j in range(len(self.kb[i])-1):
    #             if self.kb[i][j] == ">":
    #                 self.kb[i] = ["(","-"]+self.kb[i][1:j]+["|"]+self.kb[i][j+1:]
    #
    # def revised_negotion(self,str):
    #     while(True):
    #         flag = 0
    #         templist = str[:]
    #         for j in range(len(str)-1):
    #             if str[j] == "-" and str[j + 1] == "(":
    #                 mark = 1
    #                 templist[j],templist[j+1] = templist[j+1],templist[j]
    #                 for k in range(j + 2, len(str)):
    #                     if str[k] == "(":
    #                         mark += 1
    #                     if str[k] == ")":
    #                         mark -= 1
    #                     if mark == 0:
    #                         break
    #                 depth = 1
    #                 for l in range(j + 2, k):
    #                     if str[l] == "(":
    #                         depth += 1
    #                     elif str[l] == ")":
    #                         depth -= 1
    #                     if depth == 1:
    #                         if str[l] == "&":
    #                             templist[l] = "|"
    #                             templist.insert(l + 1, "-")
    #                         elif str[l] == "|":
    #                             templist[l] = "&"
    #                             templist.insert(l + 1, "-")
    #                 str = templist[:]
    #                 flag = 1
    #         if flag == 0:
    #             return str
    #
    # def revised_dbneg(self,str):
    #     while(True):
    #         flag = 0
    #         templist = str[:]
    #         for j in range(len(str)-1):
    #             if str[j] == "-" and str[j + 1] == "-":
    #                 templist.pop(j+1)
    #                 templist.pop(j)
    #                 flag = 1
    #                 break
    #         str = templist[:]
    #         if flag == 0:
    #             return str
    # def revised_dbbrackets(self,str):
    #     index = {}
    #     depth = 1
    #     while(True):
    #         flag = 0
    #         templist = str[:]
    #         for j in range(len(str)):
    #             if j not in index and str[j] == "(":
    #                 index[j] = [-1,depth]
    #                 depth += 1
    #             if j not in index and str[j] == ")":
    #                 depth -= 1
    #                 for key in range(j):
    #                     if key in index:
    #                         if index[key][1] == depth :
    #                             index[j] = [key,depth]
    #                             index[key][0] = j
    #         for i in range(len(str)):
    #             if i in index and (i+1) in index and str[i] =="(" and str[i+1] =="(":
    #                 if index[i+1][0] - index[i][0] == -1:
    #                     templist.pop(index[i+1][0])
    #                     templist.pop(i+1)
    #                     flag = 1
    #         str = templist[:]
    #         if flag == 0:
    #             return str
    #
    # def CNF(self,str):
    #     str = self.revised_dbbrackets(str)
    #     if len(str) == 3 or len(str) == 4:
    #         return str
    #     else:
    #         mark = 0
    #         for i in range(1,len(str)-1):
    #             if str[i] == "(":
    #                 mark += 1
    #             elif str[i] == ")":
    #                 mark -= 1
    #             if mark == 0:
    #                 if str[i+1]=="&":
    #                     sentence = self.CNF(str[:i+1]+[")"]) +["&"]+ self.CNF(["("]+str[i+2:])
    #                     print(sentence)
    #                     return sentence
    #                 elif str[i+1] == "|":
    #                     sentence = self.DISTR(["("]+self.CNF(str[:i+1]+[")",")"]),self.CNF(["(","("]+str[i+2:]+[")"]))
    #                     print(sentence)
    #                     return sentence
    #
    # def DISTR(self,str1,str2):
    #     str1 = self.revised_dbbrackets(str1)
    #     str2 = self.revised_dbbrackets(str2)
    #     mark = 0
    #     for i in range(len(str1)-1):
    #         if str1[i] == "(":
    #             mark += 1
    #         elif str1[i] == ")":
    #             mark -= 1
    #         if mark == 1:
    #             if str1[i+1]=="&":
    #                 sentence = self.DISTR(str1[:i+1]+[")"],str2) +["&"]+ self.DISTR(["("]+str1[i+2:],str2)
    #                 print(sentence)
    #                 return sentence
    #     mark = 0
    #     for i in range(len(str2)-1):
    #         if str2[i] == "(":
    #             mark += 1
    #         elif str2[i] == ")":
    #             mark -= 1
    #         if mark == 1:
    #             if str2[i+1]=="&":
    #                 sentence = self.DISTR(str1,str2[:i+1]+[")"]) +["&"]+ self.DISTR(str1,["("]+str2[i+2:])
    #                 print(sentence)
    #                 return sentence
    #     sentence = ["("] + str1 + ["|"] + str2 + [")"]
    #     print(sentence)
    #     return sentence