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
    # print(str)
    prove = [str[0],"!"+str[0]]     # get query variable
    evidence = str[1:]
    result = emAsk(prove,evidence,database)     # calculate the result
    print(result)

def emAsk(prove,evidence,database):
    normalize = likehood_sampling(prove,evidence,database)
    a = sum(normalize)
    for i in range(len(normalize)):     # accumulate all kinds of situation probability
        normalize[i] /= a
    return normalize

def likehood_sampling(prove,evidence1,database):
    keys = [ x for x in database.variables.keys()]
    hidden = []
    states = []
    freq = [0] * 2          # count
    sample_number = 10000   # sampling number
    for i in keys:          # generate state randomly
        if i not in evidence1:
            hidden.append(i)
            a = random.random()
            if a > 0.5:
                i = "!" + i
        states.append(i)
    for _ in range(sample_number):
        for j in hidden:
            newstates= generate(states,j,database)   # get new state
            if prove[0] in newstates:
                freq[0] += 1
            else:
                freq[1] += 1
            states = newstates[:]       # update the state
    return freq

def generate(states,variable,database):
    state0 = []     # two situation of state transition
    state1 = []
    for key in states:
        if variable in key:
            state0.append(variable)
            state1.append("!"+variable)
        else:
            state0.append (key)
            state1.append (key)
    prob0 = findprob(variable,database,state0)
    prob1 = findprob("!" + variable,database,state1)
    for i in database.nodetree:
        if i.variablename == variable:
            for j in i.children:
                name = j.variablename
                boolen,value = have_value(name,states)
                if value != 0:
                    name = "!" + name
                prob0 *= findprob(name,database,state0)
                prob1 *= findprob (name, database, state1)
    prob = [prob0, prob1]
    proba= sum(prob)
    a = random.random()     # sampling given probability
    if a > prob[0]/proba:
        return state1
    else:
        return state0



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
    query = sys.argv[2] + "|" + parserinput(sys.argv[3:])   # input information from terminal
    # query = "light-on|!family-out"
    # query = "B|J,M"
    # print(query)
    database = Db()
    database.parser(sys.argv[1])    # parser the xml document and get data
    database.createDAG()    # build the whole bayes net
    parser_query(query, database)   # parser the query sentence and get result