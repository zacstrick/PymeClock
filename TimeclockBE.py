#BackEnd
import sqlite3
from datetime import datetime as dt
from datetime import date as d
from datetime import timedelta as td
database = r'Z:\June2020.db'

# def EmployeeData():
#     con = sqlite3.connect(database)
#     cur = con.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS Emps(EmpID INTEGER PRIMARY KEY, EmpName TEXT)")
#     cur.execute("CREATE TABLE IF NOT EXISTS Swipes(EmpName TEXT, theDate DATE, theTime TIME)")
#     #cur.execute("CREATE TABLE IF NOT EXISTS VacReq(EmpName TEXT, dateApplied DATE, departure DATE, returning DATE, empComments TEXT, adminComments TEXT, approvalStatus BOOLEAN)")
#     con.commit()
#     con.close()


def Swipe(EmpID):
    # This function gets the EmpName and the EmpHrs from Emps and returns 'nobody' if they aren't in the db
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT EmpName FROM Emps WHERE EmpID=?", (EmpID,))
    tupes = cur.fetchall()
    cur.execute("SELECT EmpHrs FROM Emps WHERE EmpID=?", (EmpID,))
    tupes1 = cur.fetchall()
    con.commit()
    con.close()
    if tupes == []:
        backatcha = 'nobody'
        return backatcha
    else:
        detupled = [x[0] for x in tupes]
        detupled1 = [x[0] for x in tupes1]
        together = []
        together.append(detupled[0])
        together.append(detupled1[0])
        return together

def numberofswipes(EmpName, theDate, SwipeNO):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT SwipeNO FROM Swipes WHERE EmpName=?")

def submitToDB(EmpName, theDate, theTime, SwipeNO):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("INSERT INTO Swipes VALUES (?, ?, ?, ?)", (EmpName, theDate, theTime, SwipeNO))
    con.commit()
    con.close()

def PaidHoliday(EmpName, theDate, theTime, SwipeNO):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("INSERT INTO Swipes VALUES (?, ?, ?, ?)", (EmpName, theDate, theTime, SwipeNO))
    con.commit()
    con.close()

def addEmp(EmpID, EmpName, EmpHrs):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO Emps VALUES (?, ?, ?)", (EmpID, EmpName, EmpHrs))
    con.commit()
    con.close()

def confEmp(EmpID, EmpName):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT EmpName FROM Emps WHERE EmpID=?", (EmpID,))
    confirmation = cur.fetchall()
    con.commit()
    con.close()
    detupeconf = [x[0] for x in confirmation]
    return detupeconf
    
def onTheDayButton(EmpName, theDate):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT theTime FROM Swipes WHERE EmpName=? AND theDate=?", (EmpName, theDate))
    tupes = cur.fetchall()
    con.close()
    detuped = [x[0] for x in tupes]
    num = len(detuped)
    FMT = '%H:%M:%S'
    # ri = "\nYou're On the Clock!"
    # ro = "\nYou're Clocked Out!"
    if num == 1:
        sass = "You've got one swipe and it was at " + str(dt.strptime(detuped[0], FMT))
        return sass

    elif num == 2:
        sofar = (dt.strptime(detuped[1], FMT) - dt.strptime(detuped[0], FMT))
        sofarro = str(sofar)
        return('Clocked in: ' + str(detuped[0]) + '\nClocked out: ' + str(detuped[1]) + '\nTotal: ' + sofarro)
    
    elif num == 3:
        sofar1 = (dt.strptime(detuped[1], FMT) - dt.strptime(detuped[0], FMT))
        infromlunch = str(sofar1)
        return('Clocked in: ' + str(detuped[0]) + '\nClocked out: ' + str(detuped[1]) + '\nBack In: ' + str(detuped[2]) + '\nTotal: ' + infromlunch)
    
    elif num == 4:
        day = (dt.strptime(detuped[3], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        workday = day - lunch
        workday1 = str(workday)
        return('Clocked in: ' + str(detuped[0]) + '\nClocked out: ' + str(detuped[1]) + '\nBack In: ' + str(detuped[2]) + '\nBack Out: ' + str(detuped[3]) +'\nTotal: ' + workday1)

    elif num == 5:
        day0 = (dt.strptime(detuped[3], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch0 = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        workday0 = day0 - lunch0
        stworkday = str(workday0)
        return('Clocked in: ' + str(detuped[0]) + '\nClocked out: ' + str(detuped[1]) + '\nBack In: ' + str(detuped[2]) + '\nBack Out: ' + str(detuped[3]) +'\n..In again: ' + str(detuped[4])+'\nTotal: ' + stworkday)

    elif num == 6:
        day00 = (dt.strptime(detuped[5], FMT) - dt.strptime(detuped[0], FMT)) 
        lunch00 = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
        lunch2 = (dt.strptime(detuped[4], FMT) - dt.strptime(detuped[3], FMT))
        workday00 = day00 - (lunch00 + lunch2)
        strworkday = str(workday00)
        return('Clocked in: ' + str(detuped[0]) + '\nClocked out: ' + str(detuped[1]) + '\nBack In: ' + str(detuped[2]) + '\nBack Out: ' + str(detuped[3]) +'\n..In again: ' + str(detuped[4])+'\nAnd out again..: ' + str(detuped[5]) +'\nTotal: ' + stworkday)

def onTheDayAuto(EmpName, theDate):
    con = sqlite3.connect(database)
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
        q = "Clocked back in I guess.."
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

    
def delEmp(EmpID):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("DELETE FROM Emps WHERE EmpID=?", (EmpID,))
    con.commit()
    con.close()

##WHAT HAPPENED TO ON THE WEEK?????

# this one still needs tweaking
def inCurrently(theDate):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT EmpName FROM Swipes WHERE theDate=?", (theDate,))
    tupes = cur.fetchall()
    con.close()
    detuped = [x[0] for x in tupes]
    #num = len(detuped)
    #nodupes = set(detuped)
    counts = [(detuped.count(x),x) for x in set(detuped)]
    ins = [2,4,6]
    res = [a[1] for a in counts if a[0] not in ins]
    #for x where detuped
    for emp in res:
        return emp


def weekSummary(endofthatweek):
    formatted = dt.strptime(endofthatweek, '%Y-%m-%d')
    dformatted = formatted.date()
    startingDate = formatted - td(days=7)
    fstartingDate = startingDate.date()
    print(str(dformatted))
    print(str(fstartingDate))
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM Swipes WHERE theDate BETWEEN :starting AND :endof", {'starting': str(fstartingDate), 'endof': str(dformatted)})
    tupes = cur.fetchall()
    con.close()
    detuped = [x[0] for x in tupes]
    print(detuped)