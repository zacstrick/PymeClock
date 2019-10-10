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
          [sg.Text('', key='totalTimeOut', size=(23,1))],
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

    def tick():
        window['clock'].Update(theTime)
        time.sleep(0.2)


    event, value = window.Read()
    cardNumber = value['IN']
    if event is None:
        break 

    elif event is 'RETURN':
        nameOfSwiper = be.Swipe(cardNumber)
        be.submitToDB(nameOfSwiper, theDate, theTime)
        window['theName'].Update(nameOfSwiper)
        window['theTime'].Update(theTime)
        window['IN'].Update('')

    elif event is 'ADD':
        NewName = sg.popup_get_text('Enter New Employee Name:')
        NewCard = sg.popup_get_text('Now swipe that card of yours:')
        
        be.addEmp(NewCard, NewName)
        confirmed = be.confEmp(NewCard, NewName)
        print(confirmed,' has been added')
    
    elif event is 'REM':
        leaving = sg.popup_get_text('Swipe that card one last time please.')
        
        be.delEmp(leaving)
    
    elif event is 'totalButton':
        Empquery = sg.popup_get_text('who we lookin for')
        whatisit = be.onTheDay(Empquery, theDate)
        print(whatisit)

    else:
        sg.popup_error(title='I AM CONFUSED')
    
    tick()


        
window.Close() 
