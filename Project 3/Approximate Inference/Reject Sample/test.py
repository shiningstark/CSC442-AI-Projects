from beiyesi import *
import re
import sys,random
def parserinput(str):        # parser the input of terminal
    i = 0
    sentence = ""
    while(i<len(str)):
        sentence += str[i] + ","
        if str[i+1] == "False":
            sentence = "!" + sentence
        i += 2
        # print(i)
    sentence = sentence[:-1]
    # print(sentence)
    return sentence
def parser_query(sentence,database):         # parser the query and get result
    str = re.split(r'[\|\,]', sentence)
    prove = [str[0],"!"+str[0]]          # get query variable
    evidence = str[1:]
    result = emAsk(prove,evidence,database)     # calculate the result
    print(result)

def emAsk(prove,evidence,database):
    prob = reject_sampling(prove,evidence,database)
    # print(prob)
    a = sum(prob)
    for i in range(len(prob)):      # normalize
        prob[i] /= a
    return prob

def reject_sampling(prove,evidence,database):
    samples_number = 10000
    samples,probility = generate(database)
    for i in range(len(probility)-1):
        probility[i+1] = probility[i] + probility[i+1]
    # print(probility)
    number = [0] * len(probility)
    for j in range(samples_number):     # sample given every possible situation
        a = random.random()
        for i in range(len(probility)-1):
            if a > probility[i] and a <= probility[i+1]:
                number[i+1] += 1
            elif a <= probility[0]:
                number[0] += 1
    # print(number)
    freq = [0]*len(prove)
    for num in range(len(prove)):       # accumulate frequency for query variable
        evidence1 = evidence[:]
        evidence1.append(prove[num])
        for j in range(len(samples)):
            flag = 0
            for i in evidence1:
                if i not in samples[j]:
                    flag = 1
                    break
            if flag == 0:
                freq[num] += number[j]
    return freq


def generate(database):
    keys = [x for x in database.variables.keys()]
    value = []
    for key in keys:        # generate randomly value for every variable
        temp = []
        for i in range(2):
            if value == []:
                temp.append(str(i))
            else:
                for j in range(len(value)):
                    newvalue = value[j]+str(i)
                    temp.append(newvalue)
        value = temp[:]
    # print(len(value))
    evidences = []
    for i in range(len(value)):     # as value to generate sample
        evidence = []
        for j in range(len(value[i])):
            if value[i][j] == "0":
                evidence.append(keys[j])
            else:
                evidence.append("!" + keys[j])
        evidences.append(evidence)
    # print(evidences)
    prob = []
    for i in evidences:         # get every situation's probability
        a = emAll(keys,i,database)
        # print(a)
        prob.append(a)
    # print(prob)
    return evidences,prob

def emAll(keys,evidence,database):      # find P(x|x(parents))
    if keys == None or len(keys) == 0 :
        return 1.0
    tempkeys = keys.copy()
    variable = keys[0]
    boolen,flag = have_value(variable,evidence)     # check if the variable in evidence
    if boolen:
        tempevidence = evidence.copy()
        if variable not in evidence and "!" + variable not in evidence:
            tempevidence.append(variable)
        if flag == 0:       # given value to find probability
            return findprob(variable,database,evidence) * emAll(rest(variable,tempkeys),tempevidence,database)
        elif flag == 1:
            return findprob("!" + variable,database,evidence) * emAll(rest(variable,tempkeys),tempevidence,database)
    else:       # if not in evidence consider all situation
        tempevidence2 = evidence.copy()
        tempevidence1 = evidence.copy()
        if variable not in evidence:
            tempevidence2.append("!" + variable)
            tempevidence1.append(variable)
        return findprob(variable, database,evidence) * emAll(rest(variable, tempkeys), tempevidence1,database) + findprob("!" + variable, database,evidence) * emAll(rest(variable, tempkeys), tempevidence2,database)

def rest(variable,keys):        # remove the variable which have been assigned
    temp = keys.copy()
    temp.remove(variable)
    return temp

def have_value(variable,list):      # check if variable is in list and find the value
    temp = [variable, "!" + variable]
    for i in temp:
        if list == None:
            return False,-1
        for j in list:
            if i == j:
                if "!" in j:
                    return True,1
                else:
                    return True,0
    return False,-1

def position(indexs,value):         # as the index of given variable to find corresponding probability
    place = 0
    for i in range(len(indexs)):
        index = len(indexs) - i
        if value[i] == 1:
            place += 2 ** (index - 1)
    return place

def findprob(variable,database,evidence):       # find variable probability given evidence in the bayes net
    if "!" in variable:     # make sure the variable and value
        origin1 = variable[1:]
        value1 = "1"
    else:
        origin1 = variable
        value1 = "0"
    for i in database.nodetree:
        if i.variablename == origin1:
            if len(i.parents) != 0:     # if the variable have parents node
                indexs = []
                value = []
                for j in i.parents:
                    boolen,value2 = have_value(j.variablename,evidence)
                    if boolen:
                        indexs.append(i.given[0].index(j.variablename))
                        value.append(value2)
                index = position(indexs,value)      # find the probability place
                if value1 == "0":
                    # print(i.condpro[1][index][0])
                    return float(i.condpro[1][index][0])
                else:
                    # print(i.condpro[1][index][1])
                    return float(i.condpro[1][index][1])
            else:       # if without parents just return the probability
                if value1 == "0":
                    # print(i.condpro[1][0][0])
                    return float(i.condpro[1][0][0])
                else:
                    # print(i.condpro[1][0][1])
                    return float(i.condpro[1][0][1])


if __name__ == "__main__":
    query = sys.argv[2] + "|" + parserinput(sys.argv[3:])
    # query = "light-on|!family-out"
    # print(query)
    database = Db()
    database.parser(sys.argv[1])
    database.createDAG()
    parser_query(query, database)