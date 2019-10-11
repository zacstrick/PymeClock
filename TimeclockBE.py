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
    

def onTheDay(EmpName, theDate):
    con=sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("SELECT theTime FROM Swipes WHERE EmpName=? AND theDate=?", (EmpName, theDate))
    tupes = cur.fetchall()
    con.close()
    detuped = [x[0] for x in tupes]
    FMT = '%H:%M:%S'
    day = (dt.strptime(detuped[3], FMT) - dt.strptime(detuped[0], FMT)) 
    lunch = (dt.strptime(detuped[2], FMT) - dt.strptime(detuped[1], FMT))
    workday = day - lunch
    return workday

    
def delEmp(EmpID):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("DELETE FROM Emps WHERE EmpID=?", (EmpID,))
    con.commit()
    con.close()



EmployeeData()
