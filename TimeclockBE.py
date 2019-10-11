#BackEnd
import sqlite3
from datetime import datetime as dt
from datetime import date as d

def EmployeeData():
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Emps(EmpID INTEGER PRIMARY KEY, EmpName TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Swipes(EmpName TEXT, theDate DATE, theTime TIME)")
    con.commit()
    con.close()

def Swipe(EmpID):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("SELECT EmpName FROM Emps WHERE EmpID=?", (EmpID,))
    tupes = cur.fetchall()
    con.commit()
    con.close()
    detupled = [x[0] for x in tupes]
    return detupled[0]

def submitToDB(EmpName, theDate, theTime):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("INSERT INTO Swipes VALUES (?, ?, ?)", (EmpName, theDate, theTime))
    con.commit()
    con.close()

def addEmp(EmpID, EmpName):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO Emps VALUES (?, ?)", (EmpID, EmpName))
    con.commit()
    con.close()

def confEmp(EmpID, EmpName):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("SELECT EmpName FROM Emps WHERE EmpID=?", (EmpID,))
    confirmation = cur.fetchall()
    con.commit()
    con.close()
    return confirmation
    
def onTheDayButton(EmpName, theDate):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("SELECT theTime FROM Swipes WHERE EmpName=? AND theDate=?", (EmpName, theDate))
    tupes = cur.fetchall()
    con.close()
    detuped = [x[0] for x in tupes]
    num = len(detuped)
    FMT = '%H:%M:%S'
    ri = "\nYou're On the Clock!"
    ro = "\nYou're Clocked Out!"
    if num == 1:
        sass = "You just got here.."
        return sass

    elif num == 2:
        sofar = (dt.strptime(detuped[1], FMT) - dt.strptime(detuped[0], FMT))
        sofarro = str(sofar) + ro
        return sofarro
    
    elif num == 3:
        sofar1 = (dt.strptime(detuped[1], FMT) - dt.strptime(detuped[0], FMT))
        infromlunch = str(sofar1)+ri
        return infromlunch
    
    elif num == 4:
        day = (dt.strptime(detuped[3], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        workday = day - lunch
        workday1 = str(workday)+ro
        return workday1

    elif num == 5:
        day0 = (dt.strptime(detuped[3], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch0 = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        workday0 = day0 - lunch0
        stworkday = str(workday0)
        rsass = "\nYou're back in again I guess."
        somethin = stworkday + rsass
        return somethin

    elif num == 6:
        day00 = (dt.strptime(detuped[5], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch00 = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        lunch2 = (dt.strptime(detuped[4], FMT) - dt.strptime(detuped[3], FMT))
        workday00 = day00 - (lunch00 + lunch2)
        strworkday = str(workday00)
        a = "\nok now you're leaving, right?"
        itt = strworkday + a
        return itt

def onTheDayAuto(EmpName, theDate):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("SELECT theTime FROM Swipes WHERE EmpName=? AND theDate=?", (EmpName, theDate))
    tupes = cur.fetchall()
    con.close()
    detuped = [x[0] for x in tupes]
    num = len(detuped)
    FMT = '%H:%M:%S'
    ri = "\nClocked In!"
    ro = "\nClocked Out!"
    if num == 1:
        return ri

    elif num == 2:
        sofar = (dt.strptime(detuped[1], FMT) - dt.strptime(detuped[0], FMT))
        outforlunch = str(sofar)+ro
        return outforlunch
    
    elif num == 3:
        sofar1 = (dt.strptime(detuped[1], FMT) - dt.strptime(detuped[0], FMT))
        infromlunch = str(sofar1)+ri
        return infromlunch
    
    elif num == 4:
        day = (dt.strptime(detuped[3], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        workday = day - lunch
        workday1 = str(workday)+ro
        return workday1
        
    elif num == 5:
        q = "Woah wait why are you back?"
        return q

    elif num == 6:
        day00 = (dt.strptime(detuped[5], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch00 = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        lunch2 = (dt.strptime(detuped[4], FMT) - dt.strptime(detuped[3], FMT))
        workday00 = day00 - (lunch00 + lunch2)
        strworkday = str(workday00)
        a = "\nGood job today buddy."
        bbb = strworkday + a
        return bbb



#def onTheWeek():
    #find the dates since monday
    #take values from each of those dates
    #add them together
    #voila


    
def delEmp(EmpID):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("DELETE FROM Emps WHERE EmpID=?", (EmpID,))
    con.commit()
    con.close()



EmployeeData()
