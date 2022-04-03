from fileinput import filename
from comments import *
from reader import *
import tkinter, os, subprocess, platform
from tkinter import END
from tkinter import messagebox
import sys
import tkinter.filedialog as fd

def setMBText(text):
    MBField.delete(0,END)
    MBField.insert(0,text)

def setExpText(text):
    ExpField.delete(0,END)
    ExpField.insert(0,text)

def setOutputText(text):
    outField.delete(0,END)
    outField.insert(0,text+'-Comments')

def getMarksFile():
    currdir = os.getcwd()
    tempdir = fd.askopenfilename(parent=root, initialdir=currdir, title='Please select your markbook file', filetypes=[("Markbook file",'.csv')])
    if len(tempdir) > 0:
        courseName = tempdir[tempdir.rfind('/')+1:-4]
        setOutputText(courseName)
        setMBText(tempdir)
        return tempdir

def getExpFile():
    currdir = os.getcwd()
    tempdir = fd.askopenfilename(parent=root, initialdir=currdir, title='Please select your expectation file', filetypes=[("Excel Files",'.csv .xlsx .xls')])
    if len(tempdir) > 0:
        setExpText(tempdir)
        return tempdir

def makeExpFile():
    if MBField.get()[-4:] !='.csv' and MBField.get()[-4:] !='.xls' and MBField.get()[-4:] !='.xlsx':
        messagebox.showerror("Error","Use a csv file from markbook to generate a template")
        return None
    assignmentList = getAssessments(MBField.get())
    courseName = MBField.get()[:-4] #removes file extension
    fileName = courseName+'-Expectations'
    currdir = os.getcwd()
    i = 0
    if os.path.exists(fileName+'.csv'):
        i+=1
    while os.path.exists(fileName+"(%s).csv" % i):
        i += 1
    if i == 0:
        fileName +='.csv'
    else:
        fileName +='('+str(i) + ').csv'
    with open(fileName,'w',encoding='UTF8',newline='') as f:
        writer =csv.writer(f)
        #Standard Starter
        writer.writerow(['[Use NMs for weakness]','yes'])
        writer.writerow(['[Starters]','$ has demonstrated'])
        writer.writerow(['[Modifiers]'])
        writer.writerow(['Level 4','thorough'])
        writer.writerow(['Level 3','considerable'])
        writer.writerow(['Level 2','some'])
        writer.writerow(['Level 1','limited'])
        writer.writerow(['Level 0','very limited'])
        writer.writerow(['[Link]','knowledge of','understanding of'])
        writer.writerow(['[Demonstrators]','as demonstrated by #'])
        writer.writerow(['[Review]','$ should review'])
        writer.writerow(['[Assignments]','Expectations ->'])
        for i in assignmentList:
            writer.writerow([i])
    
    setExpText(currdir+fileName)
    if messagebox.askyesno('Open Expectation','Would you like to open the expectation file now?'):
        if platform.system()=='Darwin':
            subprocess.call('open', currdir + fileName)
        elif platform.system() == 'Windows':
            os.startfile(fileName)
        else:
                subprocess.call('xdg-open',currdir + fileName)

       


def run():
    #Make a list of the key assignments (search for non-case specific)
    #Error handling the GUI
    fileName = outField.get()
    if ExpField.get()[-4:] !='.csv':
        messagebox.showerror("Error","Use a .csv file for markbook")
        return None
    if MBField.get()[-4:] !='.csv' and MBField.get()[-4:] !='.xls' and MBField.get()[-4:] !='.xlsx':
        messagebox.showerror("Error","Use a csv, xls, or xlsx file for markbook")
        return None
    if '.' in fileName:
        messagebox.showerror("Error","you can't have a \'.\' in your file name")
    
    
    
    root.withdraw()
    #Reads the file
    rows = readExpectationsFile(ExpField.get())
    #Pulls neccessary data to build the comments.
    assignments =getExpectations(rows)
    starters = getStarters(rows)
    modifiers = getModifiers(rows)
    links = getLinks(rows)
    demonstrators = getDemos(rows)
    reviewStatements = getReview(rows)
    stdnts = readMarkbookFile(MBField.get())

    #read in student name, then grades to generate a comment
    #you would have to track the min and max grades while reading
    #constructs the student template:

    with open(fileName +'.csv','w',encoding='UTF8',newline='') as f:
        writer =csv.writer(f)
        writer.writerow(['First Name','Last Name','Best Mark','Comment'])
        for s in stdnts:
            s.cleanAssessments(assignments)
            s.comment = makeComment(starters,modifiers,links,demonstrators,reviewStatements,s.maxAssign,s.strExp,s.wknExp)

            #Add it to the list once the student is constructed, to easily loop and print to CSV for printing
            writer.writerow([s.firstName,s.lastName,s.maxAssign[0],s.comment])
    #Asks if they want to continue
    
    if messagebox.askyesno('Continue?','Would you like to continue making comment files?', icon = 'question'):
        root.deiconify()
    else:
        
        if messagebox.askyesno('Exiting application','Would you like to see the file you just made?'):
            currdir = os.getcwd()
            if platform.system()=='Darwin':
                subprocess.call('open', currdir + fileName + '.csv')
            elif platform.system() == 'Windows':
                os.startfile(fileName+'.csv')
            else:
                subprocess.call('xdg-open',currdir + fileName + '.csv')
            root.destroy()
            sys.exit(0)
        else:
            root.destroy()
            sys.exit(0)

def report_callback_exception(self, exc, val, tb):
    messagebox.showerror("Error", message=str(val))
    sys.exit(0)

#Any errors get passed back and output here as a messagebox
tkinter.Tk.report_callback_exception = report_callback_exception

#GUI
root = tkinter.Tk()
root.title('Keith Smith\'s comment starter')
root.geometry('475x200')

#Markbook file reader
insLbl1 = tkinter.Label(root,text = '1. Select the markbook file ', font =('Arial',14))
insLbl1.grid(row = 0, column = 0,columnspan=6)
MBField = tkinter.Entry(root,width=40)
MBField.grid(row=1,column=0,columnspan=6)
mbBtn = tkinter.Button(root,text = 'Markbook File',command = getMarksFile)
mbBtn.grid(row=1,column=6)

#Comment csv
insLbl2 = tkinter.Label(root,text = '2. Select the expectations file', font =('Arial',14))
insLbl2.grid(row = 2, column = 0, columnspan=6)
ExpField = tkinter.Entry(root, width = 40)
ExpField.grid(row=3,columnspan=6)
expBtn = tkinter.Button(root,text = 'Expectations File',command = getExpFile)
expBtn.grid(row = 3, column=6)

#Output field
insLbl2 = tkinter.Label(root,text = '3.Name the output file and run:', font =('Arial',14))
insLbl2.grid(columnspan=6)
outField = tkinter.Entry(root,width=40)
outField.insert(0,'output')
outField.grid(column=0)
startBtn = tkinter.Button(root,text = 'Make Comment File',command=run)
startBtn.grid(row = 5,column=6)

#Generate button
tmpltBtn = tkinter.Button(root,text="Generate Exp.\n Template", command = makeExpFile)
tmpltBtn.grid(row=1,columnspan=6,column=7)

root.mainloop()
