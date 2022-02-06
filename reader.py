
import csv
import re
from random import sample

#Globals to pass out
useNMs = False

class Assessment:
    name = "Assignment"
    def __init__ (self, name):
        self.name = name
        self.expectations = [] #Makes more sense as a list
    def addExpectation (self, exp):
        if exp != '':
            self.expectations.append(exp)

class studentFile:
    #set their max and min to narrow where marks are
    def __init__(self,lastName,firstName,studentNum):
        self.lastName = lastName
        self.firstName = firstName
        self.studentNum = studentNum
        self.maxAssign = ['',0]
        self.minAssign = ['',100]
        self.marks = []
        self.strExp = ''
        self.wknExp = ''

    #Adds a grade then updates min or max if needed
    def addGrade(self,name,mark):
        self.marks.append([name,mark]) #this could be annoying

    #Finds the max and min inside the marks list
    def getMinMax (self):
        maxList = []
        minList = []
        for m in self.marks:
            #Find max
            if m[1] > self.maxAssign[1]:
                self.maxAssign = m
                maxList = []
            elif m[1] == self.maxAssign[1]:
                if len(maxList)==0:
                    maxList.append(self.maxAssign)
                maxList.append(m)
            #Find min
            if m[1] < self.minAssign[1]:
                self.minAssign = m
                minList = []
            elif m[1] == self.minAssign[1]:
                if len(minList)==0:
                    minList.append(self.minAssign)
                minList.append(m)
        #Resolve ties with random sampling
        if len(maxList) != 0:
            self.maxAssign = sample(maxList,1)[0]
        if len(minList) != 0:
            self.minAssign = sample(minList,1)[0]

    #Builds the expectations and stores the text to use in the comment builder
    def getExpectations(self,assignments):
        maxA =Assessment("")
        minA =Assessment("")
        for a in assignments:
            if len(a.expectations)<1:
                continue
            #check if the lower cases are equivalent, not case sensitive assessments
            if a.name.lower() == self.maxAssign[0].lower():
                self.strExp = sample(a.expectations,1)[0]
                maxA = a
            if a.name.lower() == self.minAssign[0].lower():
                minA = a
                #Rolls 100 times to get a min exp
                for i in range(10):
                    self.wknExp = sample(a.expectations,1)[0]
                    if self.wknExp != self.strExp:
                        break
        if maxA.expectations == minA.expectations:
            raise Exception("Two sets of expectations are identical,\n fix this on your file and try again")
        elif self.wknExp == self.strExp:
            differentExp = set(maxA.expectations) ^ set(minA.expectations)
            sampleExp = sample(differentExp,1)[0]
            if sampleExp in maxA.expectations:
                self.strExp = sampleExp
            else:
                self.wknExp = sampleExp

        

    #Removes assignemtns not included for expectations then cleans itself
    def cleanAssessments (self,assignments):
        temp =[]
        for m in self.marks:
            for a in assignments:
                if a.name.lower() == m[0].lower():
                    #Handle NMs
                    if not useNMs and m[1]==None:
                        continue
                    elif useNMs and m[1]==None:
                        m[1] = 0
                    temp.append(m)
        self.marks = temp
        self.getMinMax()
        self.getExpectations(assignments)

    

   

        

def readMarkbookFile (filePath):
    markbookFile = csv.reader(open(filePath))
    rows = []
    rowNum = 0
    markRow = -1

    #reads in the file and stores in a table
    #Finds where the marks are with a linear search
    for row in markbookFile:
        rows.append(row)
        if '[Marks]' in row:
            markRow = rowNum
        rowNum +=1
    

    #Set values to navigate the table
    enrollment = int (rows[8][0])
    assessments = int (rows[markRow+1][1])
    
    #Builds student profiles with names and student number
    students = []
    for i in range(enrollment):
        students.append(studentFile(rows[9+i][0],rows[9+i][1],rows[9+i][2]))

    for i in range(assessments):
        assessmentName = rows[markRow+2+(i*(enrollment+1))][1]
        assessmentTotal = int(rows[markRow+2+(i*(enrollment+1))][7])
        for j in range(enrollment):
            #Handles NMs as zeroes
            if rows[markRow+3+(i*(enrollment+1))+j][1] != 'NM':
                smark = float(rows[markRow+3+(i*(enrollment+1))+j][1])
                students[j].addGrade(assessmentName,(smark/assessmentTotal)*100)
            else:
                students[j].addGrade(assessmentName,None)
    return students
    
def readExpectationsFile (filePath):
    expectationsFile = csv.reader(open(filePath))
    rows = []
    assignments = []
    global useNMs 
    #reads in the file and stores in a table
    for row in expectationsFile:
        rows.append(row)

    #Set if we use NMs
    if rows[0][1].lower()=='yes':
        useNMs = True
    #move assingment data from
    k = 0
    for i in range(2,len(rows)):
        assignments.append(Assessment(rows[i][0]))
        if assignments[k].name.isspace():
            assignments.pop()
            continue
        for j in range(1,len(rows[i])):
            assignments[k].addExpectation(rows[i][j])
        #Doesn't add assessment to the list if the forget expectations
        if  assignments[k].expectations == []:
            assignments.pop()
            continue
        k+=1
    return assignments




"""
Notes:
[x]1. NMs are treated as None, this is to eliminate it when considering max or minimum.
    Make this toggleable ->useNMs in csv
[ ]2. Not tested to use multiple mark sets
[x]3. Marks are 2D lists (x,y), x is this name, y is the actual percentage mark for easy comparisons
4. 

Edge cases:
[x]1. two max or minimums (currently selects first)
[ ]2. don't select the last used expectation pulled from the same assignment
[ ]3. Select mark or highest grade to set modifier 
[ ]4. Add customizable modifiers
[ ]5. Add customizable starters
"""