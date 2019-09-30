from beiyesi import *
import sys
import re
import random
def parserinput(str):   # parser the input of terminal
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
def parser_query(sentence,database):    # parser the query and get result
    str = re.split(r'[\|\,]', sentence)
    prove = [str[0],"!"+str[0]]     # get query variable
    evidence = str[1:]
    hidden = []
    for i in database.variables.keys():     # get hidden variable
        if i.upper() not in str and i.lower() not in str:
            hidden.append(i)
    result = emAsk(prove,evidence,database)     # calculate the result
    count = sum(result)
    for i in range(len(result)):
        result[i] /= count
    print(result)

def emAsk(prove,evidence,database):
    normalize = []
    sample_number = 10000
    for i in prove:     # put two situation of query variable into evidence
        evidence1 = evidence[:]
        evidence1.append(i)
        prob = likehood_sampling(evidence1,database)
        normalize.append(prob)
    a = sum(normalize)
    for i in range(len(normalize)):     # accumulate all kinds of situation probability
        normalize[i] /= a
    freq = [0] * 2
    for i in range(sample_number):      # sampling
        a = random.random()
        if a > normalize[0] :
            freq[1] += 1
        else:
            freq[0] += 1
    return freq

def likehood_sampling(evidence1,database):
    probability,weight = generate(evidence1,database)   # calculate the probability and weight
    likehood = 0
    for i in range(len(probability)):       # get the likehood
        likehood += probability[i] * weight[i]
    return likehood

def generate(evidence1,database):
    keys = [x for x in database.variables.keys()]
    value = []      # used for express the value of every variable
    for key in keys:        # generate the corresponding value group
        temp = []
        boolean,sign = have_value(key,evidence1)
        if not boolean:
            for i in range(2):
                if value == []:
                    temp.append(str(i))
                else:
                    for j in range(len(value)):
                        newvalue = value[j]+str(i)
                        temp.append(newvalue)
        else:
            if value == []:
                temp.append(str(sign))
            else:
                for j in range(len(value)):
                    newvalue = value[j] + str(sign)
                    temp.append(newvalue)
        value = temp[:]
    evidences = []
    weight = []
    probability = []
    for i in range(len(value)):     # as value to get evidence
        evidence = []
        for j in range(len(value[i])):
            if value[i][j] == "0":
                evidence.append(keys[j])
            else:
                evidence.append("!" + keys[j])
        evidences.append(evidence)
    for i in evidences:     # as evidence to get weight and probability
        w = float(1)
        prob = float(1)
        for j in keys:
            if j in evidence1:
                w *= emAll([j],i,database)
            else:
                prob *= emAll([j],i,database)
        weight.append(w)
        probability.append(prob)
    # print(evidences)
    # print(weight)
    # print(probability)
    return probability,weight

def emAll(keys,evidence,database):      # find P(x|x(parents))
    if keys == None or len(keys) == 0 :
        return 1.0
    tempkeys = keys.copy()
    variable = keys[0]
    boolen,flag = have_value(variable,evidence)
    if boolen:
        tempevidence = evidence.copy()
        if variable not in evidence and "!" + variable not in evidence:
            tempevidence.append(variable)
        if flag == 0:
            return findprob(variable,database,evidence) * emAll(rest(variable,tempkeys),tempevidence,database)
        elif flag == 1:
            return findprob("!" + variable,database,evidence) * emAll(rest(variable,tempkeys),tempevidence,database)
    else:
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
    if "!" in variable:
        origin1 = variable[1:]
        value1 = "1"
    else:
        origin1 = variable
        value1 = "0"
    for i in database.nodetree:
        if i.variablename == origin1:
            if len(i.parents) != 0:
                indexs = []
                value = []
                for j in i.parents:
                    boolen,value2 = have_value(j.variablename,evidence)
                    if boolen:
                        indexs.append(i.given[0].index(j.variablename))
                        value.append(value2)
                index = position(indexs,value)
                if value1 == "0":
                    # print(i.condpro[1][index][0])
                    return float(i.condpro[1][index][0])
                else:
                    # print(i.condpro[1][index][1])
                    return float(i.condpro[1][index][1])
            else:
                if value1 == "0":
                    # print(i.condpro[1][0][0])
                    return float(i.condpro[1][0][0])
                else:
                    # print(i.condpro[1][0][1])
                    return float(i.condpro[1][0][1])

# the entrance for the program
if __name__ == "__main__":
    # query = sys.argv[2] + "|" + parserinput(sys.argv[3:])   # input information from terminal
    query = "light-on|family-out"
    # query = "B|J,M"
    # print(query)
    database = Db()
    database.parser('sys.argv[1]')    # parser the xml document and get data
    database.createDAG()    # build the whole bayes net
    parser_query(query, database)   # parser the query sentence and get result