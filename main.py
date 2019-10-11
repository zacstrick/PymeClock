import sys
import datetime
import PySimpleGUI as sg
import time
import TimeclockBE as be

# here we go with the window
layout = [[sg.Text('Swipe Your Card')],
          [sg.InputText(size=(6,1), key='IN', focus=True)], [sg.Text('', key='clock', size=(8,1), font=('arial', 20, 'bold'))],
          [sg.Text('', key='theName', size=(45,1))],
          [sg.Text('', key='theTime', size=(45,1))],
          [sg.Text('', key='totalTimeOut', size=(23,2))],
          [sg.Button('', key='RETURN', visible=False, bind_return_key=True)], [sg.Button('New Employee Add', key='ADD')], 
          [sg.Button('Remove Employee', key='REM')], [sg.Button('Total Today', key='totalButton')]]

window = sg.Window('Clock!', layout)


def clearfields():
    window['theName'].Update('')
    window['theTime'].Update('')


while True :

    # so here are the time vars
    rightNow = datetime.datetime.now()
    theTime = rightNow.strftime("%H:%M:%S")
    theDate = rightNow.strftime("%Y-%m-%d")

    event, value = window.Read(timeout=100)

    if event == None:
        break 
    cardNumber = value['IN']
    if event == 'RETURN':
        nameOfSwiper = be.Swipe(cardNumber)
        be.submitToDB(nameOfSwiper, theDate, theTime)
        totd = be.onTheDayAuto(nameOfSwiper, theDate)
        window['theName'].Update(nameOfSwiper)
        window['theTime'].Update(theTime)
        window['totalTimeOut'].Update(totd)
        window['IN'].Update('')

    elif event == 'ADD':
        NewName = sg.popup_get_text('Enter New Employee Name:')
        NewCard = sg.popup_get_text('Now swipe that card of yours:')
        
        be.addEmp(NewCard, NewName)
        confirmed = be.confEmp(NewCard, NewName)
        print(confirmed,' has been added')
    
    elif event == 'REM':
        leaving = sg.popup_get_text('Swipe that card one last time please.')
        
        be.delEmp(leaving)
    
    elif event == 'totalButton':
        Empswipe = sg.popup_get_text('Alright, swipe your card.')
        Empquery = be.Swipe(Empswipe)
        whatisit = be.onTheDayButton(Empquery, theDate)
        sg.popup_quick(whatisit, auto_close_duration=3, no_titlebar=True, font=('arial', 16, 'bold'))

    window['clock'].Update(theTime)
        
window.Close() 
