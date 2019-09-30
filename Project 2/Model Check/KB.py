import re
class KB: # structure of kb
    def __init__(self):
        self.kb = []  # original sentence
        self.table =[] # variables

    def tell(self,sentence): # parser the sentence and tranform them into kb base and table
        # element = self.parser(sentence)
        # self.kb.append(element)
        # self.revised()
        clause,items = self.parser(sentence)
        for i in clause:
            if i not in self.kb:
                self.kb.append(i)
        for i in items:
            if i not in self.table:
                self.table.append(i)
    def ask(self,sentence): # use binary number to represent the variable, 0 represent false, 1 represent true
        # self.tell(sentence)
        a = 2**len(self.table)-1    # the binary number
        result = a+1                # the number of possible models
        while(a>=0):                # model check
            b = list(bin(a)[2:])    # the binary format
            while len(b)<len(bin(2**len(self.table)-1)[2:]):    # make up 0 for the total binary format into the head
                b.insert(0,"0")
            if self.check(b) == 0:          # check function is to check if the model is satisfied
                str = re.split(r'[\(\)\|]',sentence)    # tranform the sentence needed to prove, which include negation
                str = [x for x in str if x != ""]
                count = len(str)                        # the number of variable in the sentence
                for j in str:
                    c = re.split(r'[\-]', j)
                    c = [x for x in c if x != ""]
                    if b[self.table.index(c[0])] == "0" and "-" not in j:   # check if the model can make the variable true
                        count -= 1
                    elif b[self.table.index(c[0])] == "1" and "-" in j:
                        count -= 1
                    if count == 0:      # if all variables are false, so the sentence can not be proved
                        print(sentence+" is false!!")
                        return
            else:       # if the model is false, check next one
                result -= 1
            a -= 1
        if result == 0: # if no model is fine, so no conclusion
            # self.delete()
            print("no conclusion!!")
        else:   # if there is a model, so the sentence is truth
            print(sentence + " is truth!!")

    def delete(self):
        self.kb.pop()

    def parser(self,sentence):  # parser the sentence
         # a = re.split(r'([\-\^\&\(\)\>\=])', sentence)
         a = re.split(r'[\&]', sentence)
         b = re.split(r'[\-\|\&\(\)\>\=]', sentence)
         return [x for x in a if x!=''],[x for x in b if x!='']

    def check(self,a):      # check if the model satisfies the kb
        for i in self.kb:   # for every sentence in kb
            b = re.split(r'[\(\)\|]',i)
            b = [x for x in b if x !=""]
            count = len(b)
            for j in b:
                c = re.split(r'[\-]',j)
                c = [x for x in c if x != ""]
                if a[self.table.index(c[0])] == "0" and "-" not in j:
                    count -= 1
                elif a[self.table.index(c[0])] == "1" and "-" in j:
                    count -= 1
                if count == 0:
                    return 1    # if the sentence is false, so the kb is false
        return 0
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