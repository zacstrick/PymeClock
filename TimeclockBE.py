#BackEnd
import sqlite3

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
    returnedValue = cur.fetchall()
    con.commit()
    con.close()
    delisted = ''.join(map(str, returnedValue))
    stripped = str(delisted).strip('()')
    strippedAgain = str(stripped).strip(',')
    swiperName = str(strippedAgain).strip("''")
    return swiperName

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
    timeses = cur.fetchall()
    con.close()
    return timeses

    
def delEmp(EmpID):
    con = sqlite3.connect('Timeclock.db')
    cur = con.cursor()
    cur.execute("DELETE FROM Emps WHERE EmpID=?", (EmpID,))
    con.commit()
    con.close()


EmployeeData()