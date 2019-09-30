import re
from KB import KB
knowledge = KB()

a11 = ["p","-p|q"] # problem 1
a21 = ["-p11","-b11|p12|p21","-b21|p11|p22|p31","-b11","b21","b11|-p12","b11|-p21","b21|-p11","b21|-p22","b21|-p31"] # problem 2
a31 = ["-my|-mo","my|mo","my|ma","mo|h","-ma|h","-h|mg"] # problem 3
a41 = ["b|c","-b|-c","-a","-c|b|-a","c|-b","a|c"] # problem 4(1)
a42 = ["b|-c","-b|c","-a|b|-c","-b|a","-c|-a","a|c"] # problem 4(2)
a51 = ["b|-a|-l","-b|a","-b|l","c|-b|-g","-c|b","-c|g","d|-e|-l","-d|e","-d|l","f|-d|-i","-f|d","-f|i",
     "e|-c|-h","-e|c","-e|h","g|e|j","-g|-j","-g|-e","h|f|k","-h|-f","-h|-k","i|g|k","-i|-g","-i|-k",
     "j|a|c", "-j|-a", "-j|-c","k|d|f","-k|-d","-k|-f","l|b|j","-l|-b","-l|-j",] # problem 5
a61 = ["a|-x","-a|x","b|-y","b|-z","-b|y|z","c|-a|-b","-c|a","-c|b","d|-x|-y","-d|x","-d|y","e|-x|-z","-e|x","-e|z",
     "-f|d|e","f|-d","f|-e","g|-f","g|c","-g|-c|f","h|-g","-g|a","x|y|z|w"] # problem 6(1)
a62 = ["a|-x","-a|x","h|-g","-g|a","g|-??","g|c","-g|-c|??","c|-a|-?","-c|a","-c|?","x|y|z|w"] # problem 6(2)
b11 = ["q"] # problem 1
b21 = ["p12"] # problem 2
b31 = ["my","mg","h"] # problem 3
b41 = ["a","b","c"] # problem 4
b51 = ["a","b","c","d","e","f","g","h","i","j","k","l"]# problem 5
b61 = ["a","b","c","d","e","f","g","h","x","y","z","w"]# problem 6(1)
b62 = ["a","c","g","h","x","y","z","w"]# problem 6(2)
a = {1:[a11],2:[a21],3:[a31],4:[a41,a42],5:[a51],6:[a61,a62]}
b = {1:[b11],2:[b21],3:[b31],4:[b41,b41],5:[b51],6:[b61,b62]}

if __name__ == "__main__":
    while (True):
        print("which problem do you want to solve(please type 1-6): ")
        number1 = int(input())
        if not number1 < 7 or not number1 > 0:
            print("\ninvalid input!! Please retype\n")
        else:
            print("which subproblem do you want to solve(please type 1-2): ")
            number2 = int(input())-1
            if not number2 < len(a[number1]) or not number2 >= 0:
                print("\ninvalid input!! Please retype\n")
            else:
                break
    for j in a[number1][number2]:
        knowledge.tell(j)           # input the truth into kb
    # print(knowledge.table)          # print all the variables in kb
    for i in b[number1][number2]:
        knowledge.ask(i)            # ask kb if the clause is truth
        # print(knowledge.model)      # print the model (every number in the string represent the value of variable,
                                    # 0: false  1: truth by using dpll)
        flag = 0
        if len(knowledge.model)>0:
            cord = knowledge.table.index(i)     # if there is model, find the index of variable
            # print(cord)
            for j in knowledge.model:
                if cord < len(j) and j[cord] == "0":
                    print(i + " is false!!")
                    flag = 1
                    break
            if cord >= len(j):      # if tree do not assign the value, so it is no matter what value is, so it has no conclusion
                print(i+" has no conclusion")
            elif flag == 0:
                print(i + " is truth!!")        # if unproved variable is true in every model, it will be proved,
                                            # otherwise it is false
        knowledge.model = []                # avoid printing model repeat