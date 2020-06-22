#R&S Employee Timekeeping System
#Written by Zac Strickland

import sys
import datetime
import PySimpleGUI as sg
import time
import TimeclockBE as be
import week
import random
from keypad import keypadd

dbdb = be.database

sg.theme("SandyBeach")

layout = [[sg.Text('Swipe Your Card', font=('arial', 16, 'bold'))],
          [sg.InputText(size=(6,1), key='IN', focus=True), sg.Button('Submit Time', key='RETURN', visible=False, bind_return_key=True)], 
          [sg.Button('Manual Input', key='MAN')], [sg.Button('Clear Input Field', key='CLR')], [sg.Text('', key='clock', size=(7,1), font=('arial', 20, 'bold',))],
          [sg.Text('', key='theName', size=(18,1), justification="center")],
          [sg.Text('', key='theTime', size=(18,1), justification="center")],
          [sg.Text('', key='totalTimeOut', size=(23,2), justification="center")], [sg.Button('Hours Clocked Since Monday', key='WEEK')],
          [sg.Button('New Employee Add', key='ADD', visible=False)], [sg.Button('Flyby', key='FLY', visible=False)],
          [sg.Button('Remove Employee', key='REM', visible=False)], [sg.Button('Total Today', size=(20,2), key='totalButton')]]

window = sg.Window('R&S Employee Timekeeping System', layout, element_justification='center')

def returnd(cardNumber):
    swipername_overnightstatus = be.Swipe(cardNumber)
    swipername = swipername_overnightstatus[0]
    overnightstatus = swipername_overnightstatus[1]
    print(swipername)
    if swipername == '':
        sg.popup_quick("Oops! You aren't in the Database yet. \nAdd yourself with the button.", no_titlebar=True, auto_close_duration=3, font=('arial', 12, 'bold'))
        window['IN'].Update('')
    elif swipername == 'n':
        window['IN'].Update('')
        window['theName'].Update('')
        window['theTime'].Update('')
        window['totalTimeOut'].Update('')
    elif swipername == 'John Reeves':
        be.submitToDB(swipername, theDate, theTime, '0')
        totd = be.onTheDayAuto(swipername, theDate)
        sg.popup_quick(chirp, no_titlebar=True, auto_close_duration=1.2, font=('arial', 12, 'bold'))
        window['theName'].Update(swipername)
        window['theTime'].Update(theTime)
        window['totalTimeOut'].Update(totd)
        window['IN'].Update('')
    elif swipername == 'Jim Stockglausner':
        be.submitToDB(swipername, theDate, theTime, '0')
        totd = be.onTheDayAuto(swipername, theDate)
        sg.popup_quick("ALL HAIL JIM OF THE BRASS SPHERE", no_titlebar=True, auto_close_duration=2.5, font=('arial', 12, 'bold'))
        window['theName'].Update(swipername)
        window['theTime'].Update(theTime)
        window['totalTimeOut'].Update(totd)
        window['IN'].Update('')
    # elif swipername == 'Nick Woolbright':
    #     be.submitToDB(swipername, theDate, theTime, '0')
    #     totd = be.onTheDayAuto(swipername, theDate)
    #     sg.popup_quick("Welcome back fuckface", no_titlebar=True, auto_close_duration=1.5, font=('arial', 12, 'bold'))
    #     window['theName'].Update(swipername)
    #     window['theTime'].Update(theTime)
    #     window['totalTimeOut'].Update(totd)
    #     window['IN'].Update('')
    else:
        if overnightstatus == 'False':
            be.submitToDB(swipername, theDate, theTime, '0')
            totd = be.onTheDayAuto(swipername, theDate)
            window['theName'].Update(swipername)
            window['theTime'].Update(theTime)
            window['totalTimeOut'].Update(totd)
            window['IN'].Update('')
        else:
            be.submitToDB(swipername, theDate, theTime, '0')
            totd = be.onTheDayAuto(swipername, theDate)
            window['theName'].Update(swipername)
            window['theTime'].Update(theTime)
            window['totalTimeOut'].Update(totd)
            window['IN'].Update('')

    
while True:

    rightNow = datetime.datetime.now()
    theTime = rightNow.strftime("%H:%M:%S")
    theDate = rightNow.strftime("%Y-%m-%d")
    listofchirps = open('lkq.txt').read().splitlines()
    chirp = random.choice(listofchirps)

    event, value = window.Read(timeout=100)

    if event == None:
        break 
    
    cardNumber = value['IN']
    if event == 'RETURN':
        returnd(cardNumber)

    elif event == 'ADD':
        NewName = sg.popup_get_text('Swipe up from the bottom and select the OnScreen Keyboard\nSymbol right next to the time and date on the right\nThen, Enter New Employee Name:', no_titlebar=True)
        OvernightsYN = sg.popup_yes_no('Are you working overnights or\n do you ever plan to ever work past midnight?')
        print(OvernightsYN)
        NewCard = sg.popup_get_text('Now swipe that card of yours:', no_titlebar=True)
        be.addEmp(NewCard, NewName, OvernightsYN)
        confirmed = be.confEmp(NewCard, NewName)
        peeled = [x[0] for x in confirmed]
        addconf = str(confirmed) + ' has been added'
        sg.popup_quick(addconf, font=('arial', 12, 'bold'), no_titlebar=True, auto_close_duration=3)

    elif event == 'CLR':
        window['IN'].Update('')
    
    elif event == 'MAN':
        manenter = keypadd()
        returnd(manenter)

    elif event == 'REM':
        leaving = sg.popup_get_text('Swipe that card one last time please.')
        areYouSure = be.Swipe(leaving)
        pops = sg.popup_yes_no('Are you sure you want to remove '+ areYouSure)
        if pops == 'Yes':
            be.delEmp(leaving)
            areTheyGone = be.Swipe(leaving)
            if areTheyGone == 'nobody':
                sg.popup_quick(areYouSure + ' has been removed from the database')
            else:
                sg.popup_quick("hm.. that didn't work for some reason")
        else:
            sg.popup_quick("Ok make up your mind and get back to me.") 
    
    elif event == 'totalButton':
        Empswipe = sg.popup_get_text('Alright, swipe your card.')
        Empquery = be.Swipe(Empswipe)
        whatisit = be.onTheDayButton(Empquery[0], theDate)
        sg.popup_quick(whatisit, auto_close_duration=5, no_titlebar=True, font=('arial', 16, 'bold'))
    
    elif event == 'FLY':
        Empswipe = sg.popup_get_text('Sup, bud.\nSwipe your card.')
        print(Empswipe)
        Empquery = be.Swipe(Empswipe)
        print(Empquery)
        be.submitToDB(Empquery[0], theDate, theTime, '0')
        hourlater = rightNow + datetime.timedelta(hours=1)
        be.submitToDB(Empquery[0], theDate, hourlater.strftime("%H:%M:%S"), '0')
        sg.popup_quick_message("Alright, an hour's been recorded.")
        
    
    elif event == 'WEEK':
        tooday = datetime.date.today()
        mondaycalc = tooday - datetime.timedelta(days=tooday.weekday())
        print(mondaycalc)
        swipey = sg.popup_get_text('Alright, swipe your card.')
        print(swipey)
        if swipey == None:
            sg.popup_quick_message("k then", auto_close_duration=.5)
        elif swipey == '':
            sg.popup_quick_message("I said\nSWIPE YOUR CARD", auto_close_duration=.5)
        else:
            Empqueryy = be.Swipe(swipey)
            whatisit = week.OTW(str(mondaycalc), str(tooday), dbdb, emp=Empqueryy[0])
            sg.popup_quick_message(str(whatisit[0]), auto_close_duration=3)

    window['clock'].Update(theTime)
        
window.Close() 
