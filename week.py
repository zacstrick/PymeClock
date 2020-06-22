from contextlib import redirect_stdout as redir
import sqlite3
# from TimeclockBE import database as db
import time
import datetime as dt
from datetime import timedelta as td
#from DBCre8 import theDate as d8
import TimeclockBE as be
import calendar
import sys
import PySimpleGUI as sg
import os


db = be.database


def loggy(ttext):
    loggo = open('loggyss.txt', 'a+')
    loggo.write(str(ttext)+'\n')
    loggo.close



def ddotw(ddate):
    stripped = dt.datetime.strptime(ddate, '%Y-%m-%d').weekday()
    return calendar.day_name[stripped]

def dateMath(num, detuped):
    FMT = '%H:%M:%S'
    
    if num == 0:
        pass
    elif num == 1:
        pass
    elif num == 2:
        sofar = (dt.datetime.strptime(detuped[1], FMT) - dt.datetime.strptime(detuped[0], FMT))
        if sofar >= dt.timedelta(hours=8):
            lunch = dt.timedelta(minutes=30)
            sofar = sofar - lunch
            return str(sofar)
        return str(sofar)    
    elif num == 3:
        sofar = (dt.datetime.strptime(detuped[2], FMT) - dt.datetime.strptime(detuped[0], FMT))
        if sofar >= dt.timedelta(hours=8):
            lunch = dt.timedelta(minutes=30)
            sofar = sofar - lunch
            return str(sofar)
        return str(sofar)
    elif num == 4:
        day = (dt.datetime.strptime(detuped[3], FMT) - dt.datetime.strptime(detuped[0], FMT)) 
        lunch = (dt.datetime.strptime(detuped[2], FMT) - dt.datetime.strptime(detuped[1], FMT)) 
        if day >= dt.timedelta(hours=8):
            if lunch >= dt.timedelta(minutes=30):
                pass
            else:
                lunch = dt.timedelta(minutes=30)
                pass
        else:
            pass
        workday = day - lunch
        return str(workday)
    elif num == 5:
        day = (dt.datetime.strptime(detuped[3], FMT) - dt.datetime.strptime(detuped[0], FMT)) 
        lunch = (dt.datetime.strptime(detuped[2], FMT) - dt.datetime.strptime(detuped[1], FMT))
        if day >= dt.timedelta(hours=8):
            if lunch >= dt.timedelta(minutes=30):
                pass
            else:
                lunch = dt.timedelta(minutes=30)
                pass
        else:
            pass
        workday = day - lunch
        return str(workday)
    elif num == 6:
        day = (dt.datetime.strptime(detuped[5], FMT) - dt.datetime.strptime(detuped[0], FMT)) 
        lunch1 = (dt.datetime.strptime(detuped[2], FMT) - dt.datetime.strptime(detuped[1], FMT))
        lunch2 = (dt.datetime.strptime(detuped[4], FMT) - dt.datetime.strptime(detuped[3], FMT))
        lunch = lunch1 + lunch2
        if day >= dt.timedelta(hours=8):
            if lunch >= dt.timedelta(minutes=30):
                pass
            else:
                lunch = dt.timedelta(minutes=30)
                pass
        else:
            pass
        workday = day - lunch
        return str(workday)

def x_round(x):
    return round(x*4)/4

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + td(n)

def secondshift(EmpName):
    con = sqlite3.connect(db)
    print(EmpName)
    cur = con.cursor()
    cur.execute("SELECT EmpHrs FROM Emps WHERE EmpName=?", (EmpName,))
    empshift = cur.fetchone()
    cur.close()
    empshift = [x[0] for x in empshift]
    print(empshift[0])
    return empshift[0]


def OTW(sow, eow, dataBase, emp=None):
    #BEFORE we start let's delete the previous Loggy:
    if os.path.exists('loggy.txt'):
        os.remove('loggy.txt')
    #first, let's get every day between sow and eow; the datelist
    loggy('This will be for times logged between ' + str(sow) + ' and ' + str(eow) + '\n')
    sdate = dt.datetime.strptime(sow, '%Y-%m-%d')
    edate = dt.datetime.strptime(eow, '%Y-%m-%d')
    datelist = []
    for times in daterange(sdate, edate):
        datelist.append(times.strftime("%Y-%m-%d"))

    #was a name specified? No?
    if emp == None:
        con = sqlite3.connect(dataBase)
        cur = con.cursor()
        cur.execute("SELECT EmpName FROM Emps WHERE EmpHrs='False'")
        uemps = cur.fetchall()
        cur.close()
        emps = [x[0] for x in uemps]
        emps = sorted(emps, key=lambda x: x.split(" ")[-1])
        loggy(emps)
        loggy('\n')

        #and so begins the looping
        namesandtotw = []
        for emp in emps: 
            totlist = []
            
            loggy(emp)

            for d8 in datelist:
                con = sqlite3.connect(dataBase)
                cur = con.cursor()
                cur.execute("SELECT theTime FROM Swipes WHERE EmpName=? AND theDate=?", (emp, d8))
                tupes = cur.fetchall()
                con.close()
                detuped = [x[0] for x in tupes]
                sordt = sorted(detuped)
                loggy(ddotw(d8) + ', ' + str(d8))
                loggy(sordt)
                num = len(sordt)
                if (num % 2) == 0:
                    pass
                else:
                    loggy("\n^^^^^^^^^^^^^^^^^^^^^^^^^^<---------------------------------UNEVEN # OF SWIPES")

                tt = dateMath(num, sordt)
                if tt == None:
                    tt = '00:00:00'

                totlist.append(tt)
            totalSecs = 0
            loggy("Totals:")
            loggy(totlist)
            for tm in totlist:
                timeParts = [int(s) for s in tm.split(':')]
                totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
            totalSecs, sec = divmod(totalSecs, 60)
            hr, min = divmod(totalSecs, 60)
            tttt = "%d:%02d:%02d" % (hr, min, sec)
            (h, m, s) = tttt.split(':')
            result = int(h) * 3600 + int(m) * 60 + int(s)
            tdec = result / 3600
            rtdec = round(tdec, 2)
            xrtdec = x_round(rtdec)
            sxrtdec = str(xrtdec)
            all3 = emp + ': ' + tttt + ' or ' + sxrtdec
            namesandtotw.append(all3)
            loggy(tttt + " or " + sxrtdec + '\n')
            # namesandtotw.append(tttt)
        return namesandtotw

    #  oh you DID specify a name??
    else:
        #then we looping
        namesandtotw = []
        totlist = []
        print(datelist)
        for d8 in datelist:
            con = sqlite3.connect(dataBase)
            cur = con.cursor()
            cur.execute("SELECT theTime FROM Swipes WHERE EmpName=? AND theDate=?", (emp, d8))
            tupes = cur.fetchall()
            con.close()
            detuped = [x[0] for x in tupes]
            sordt = sorted(detuped)
            print(ddotw(d8) + ', ' + str(d8))
            print(sordt)
            num = len(sordt)
            if (num % 2) == 0:
                pass
            else:
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^<---------------------------------UNEVEN # OF SWIPES\n")

            tt = dateMath(num, sordt)
            if tt == None:
                tt = '00:00:00'

            totlist.append(tt)
        totalSecs = 0
        print(totlist)
        for tm in totlist:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        tttt = "%d:%02d:%02d" % (hr, min, sec)
        (h, m, s) = tttt.split(':')
        result = int(h) * 3600 + int(m) * 60 + int(s)
        tdec = result / 3600
        print(str(tdec) + " <tdec")
        rtdec = round(tdec, 2)
        xrtdec = x_round(rtdec)
        sxrtdec = str(xrtdec)
        all3 = emp + ': ' + tttt + ' or ' + sxrtdec
        namesandtotw.append(all3)
        print(all3)
        # namesandtotw.append(tttt)
        return namesandtotw


def otwreport(name, datee1, datee2):

    with open(f'reports/{name}_{datee1}-{datee2}.txt', 'w+') as fyle:
        with redir(fyle):
            fyle.write(str(OTW(datee1, datee2, db, name)))
    fyle.close()

# otwreport('Zac Strickland', '2020-06-01', '2020-06-07')