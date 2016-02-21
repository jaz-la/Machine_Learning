from math import log

def isFloat(value):
  try:
    float(value)
    return True
  except:
    return False

def isInt(value):
  try:
    int(value)
    return True
  except:
    return False


def cal_I(value):
    if value > 1:
        print "error value" 
        return -1
    #print "value is :",value 
    if(value > 1.0 or value < 0.0):
        print "error value in cal_I"
        return -1
    if value == 1.0 or value == 0.0:
        return 0.0
    ret = (- (value * log(value,2.0))) - (1.0-value) * log((1.0-value), 2.0)
    #print ret 
    return ret

def isNum(value):
    return isInt(value) or isFloat(value)

class Node:
    def __init__(self):
        self.col = -1 # split data base on which col
        self.data = [] # filtered temporary data 
        self.result = None # classification result
        self.splitPoints = [] # split points
        self.used_col = [] # col used by its parent or ancestor
        self.children = {} # children dict, each element in children is a node

    def set_best_entropy_col(self):
        best_remainder = 999.0
        for column in range(len(self.data[0]) -1 ):
            used = False
            for j in self.used_col:
                if column == j:
                    used = True

            if not used:

                remainder = 0.0
                countDict = {}
                if not isNum(self.data[0][column]):
                    for line in self.data:
                        if line[column] in countDict:
                            if line[-1] == "+":
                                countDict[line[column]]["pos"] += 1
                            else:
                                countDict[line[column]]["neg"] += 1
                        else:
                            countDict[line[column]] = {}
                            countDict[line[column]]["pos"] = 0
                            countDict[line[column]]["neg"] = 0
                            if line[-1] == "+":
                                countDict[line[column]]["pos"] += 1
                            else:
                                countDict[line[column]]["neg"] += 1
                    for key in countDict:
                        sum = float((countDict[key]["pos"] + countDict[key]["neg"]))
                        pos = float(countDict[key]["pos"])
                        neg = float(countDict[key]["neg"])
                        all = float(len(self.data))
                        #print "key:",key,"sum:",sum,"pos",pos,"neg",neg,"all",all
                        remainder += sum / all * cal_I(pos/sum)
                    print "remainder is :",remainder,"col number:",column
                    if remainder < best_remainder:
                        self.splitPoints = []
                        print "new remainder is :",remainder,"old remainder is",best_remainder,"col number:",column
                        for key in countDict:
                            # print key
                            self.splitPoints.append(key)
                        self.col = column
                        best_remainder = remainder
                else:
                    for line1 in self.data:
                        used = False
                        point =line1[column]
                        remainder = 0.0
                        gePos = 0
                        lPos = 0
                        geNeg = 0
                        lNeg = 0
                        for line in self.data:
                            if line[column] >= point:
                                if line[-1] == "+":
                                    # countDict["ge"]["pos"] += 1
                                    gePos += 1
                                else:
                                    # countDict["l"]["neg"] += 1
                                    geNeg += 1
                            else:
                                if line[-1] == "+":
                                    # countDict["ge"]["pos"] += 1
                                    lPos += 1
                                else:
                                    # countDict["l"]["neg"] += 1
                                    lNeg += 1
                        if(lPos + lNeg == 0) or (gePos + geNeg == 0):
                            pass
                        else:
                            # print "gePos:",gePos,"geNeg:",geNeg
                            sum = float(gePos + geNeg)
                            pos = float(gePos)
                            neg = float(geNeg)
                            all = float(len(self.data))
                            # print all
                            remainder += sum / all * cal_I(pos/sum)
                            sum = float(lPos + lNeg)
                            pos = float(lPos)
                            neg = float(lNeg)
                            all = float(len(self.data))
                            # print all
                            remainder += (sum / all) * cal_I(pos/sum)
                            if remainder < best_remainder:
                                self.col = column
                                print "new remainder is :",remainder,"old remainder is",best_remainder,"col number:",column
                                best_remainder = remainder
                                self.splitPoints = [point]
                    print "remainder is :",remainder,"col number:",column
            else:
                print "cannot use ",column
        if self.col == -1:
            print "have some data which cannot be classified,data len:",len(self.data)
            print self.used_col
        # for line in self.data:
        #     exist = False
        #     for elmt in self.splitPoints: 
        #         if(line[self.col] == elmt):
        #             exist = True
        #     if not exist:
        #         self.splitPoints.append(line[self.col])

    def expand(self):
        # print "data size:",len(self.data),"col:",self.col
        print "new expand"
        for line in self.data:
            print line
        tmp_result = self.data[0][-1]
        need_expand = False
        for i in range(1,len(self.data)):
            if self.data[i][-1] != tmp_result:
                need_expand = True

        if need_expand:
            self.set_best_entropy_col()
            if self.col < 0:
                print "error col number"
                return 0


            print self.col
            if(len(self.splitPoints) == 1): # a number

                c1 = Node()
                c1.used_col = self.used_col[:]
                c1.used_col.append(self.col)


                c2 = Node()
                c2.used_col = self.used_col[:]
                c2.used_col.append(self.col)

                for line in self.data:
                    if(line[self.col] >= self.splitPoints[0]):
                        c2.data.append(line)
                    else:
                        c1.data.append(line)
                self.children["ge"] = c2
                self.children["l"] = c1
            else:
                print "splitPoints length:",len(self.splitPoints)
                for sp in self.splitPoints:
                    c = Node()
                    c.used_col = self.used_col[:]
                    c.used_col.append(self.col)
                    for line in self.data:
                        if(line[self.col] == sp):
                            c.data.append(line)
                    self.children[sp] = c
                    print "child appended, data length:",len(c.data)

            self.data = []    
            for key in self.children:
                print key
                self.children[key].expand()

        else:
            self.result = tmp_result
            self.data = []

    def check(self,line):
        if self.result != None:
            if line[-1] == self.result:
                return True
            else:
                return False
        if self.result == None and len(self.children) == 0:
            print "cannot make decision"
            return False
        if(len(self.splitPoints) == 1):
            # number here
            if line[self.col] >= self.splitPoints[0]:
                return self.children["ge"].check(line)
            else:
                return self.children["l"].check(line)
        else:
            if line[self.col] in self.children:
                return self.children[line[self.col]].check(line)
            else:
                return False



def main():
    data = []
    data_size = 0.0
    with open("crx.data.txt", 'r') as fp:
        for line in fp:
            data_size += 1.0
            if "?" not in line:
                data.append(line.strip().replace(';', '').split(','))
    root = Node()
    root.data = data
    root.expand()

    # decision tree is constructed, run test data
    fail = 0.0
    succed = 0.0
    test_size = 0.0
    with open("crx.data.test.txt", 'r') as fp:
        for line in fp:
            test_size += 1.0
            if "?" not in line:
                ret = root.check(line.strip().replace(';', '').split(','))
                if ret == True:
                    succed += 1.0
                else:
                    fail += 1.0
            else:
                fail += 1.0
                
    print "succed:",succed,"fail:",fail,"tranning data:",data_size,"test data:",test_size,"rate:",succed/(succed+fail)
    

    return 0

if __name__ == "__main__":
    main()