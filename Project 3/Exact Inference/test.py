from beiyesi import *
import re
import sys
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
    normalize = []
    a = float(0)
    keys =[x for x in database.variables.keys()]
    for i in prove:
        evidence1 = evidence[:]
        evidence1.append(i)
        prob = emAll(keys,evidence1,database)       # regard query variable as part of evidence
        normalize.append(prob)
        a += prob
    # print(a)
    for j in range(len(normalize)):         # normalize
        normalize[j] /= a
    return normalize

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
    database.parser(sys.argv[1])        # parser query
    database.createDAG()                # create bayes net
    parser_query(query, database)       # get result