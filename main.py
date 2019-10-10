import csv
import sys
import datetime
import PySimpleGUI as sg

# here we go with the window
layout = [[sg.Text('Swipe Your Card')],
          [sg.InputText(size=(6,1), key='IN', focus=True)],
          [sg.Text('', key='theName', size=(45,1))],
          [sg.Text('', key='theTime', size=(45,1))],
          [sg.Button('', key='RETURN', visible=False, bind_return_key=True)]]

window = sg.Window('Clock!', layout)import sys
import datetime
import PySimpleGUI as sg
import time
import TimeclockBE as be

# here we go with the window
layout = [[sg.Text('Swipe Your Card')],
          [sg.InputText(size=(6,1), key='IN', focus=True)],
          [sg.Text('', key='theName', size=(45,1))],
          [sg.Text('', key='theTime', size=(45,1))],
          [sg.Text('', key='totalTimeOut', size=(23,1))],
          [sg.Button('', key='RETURN', visible=False, bind_return_key=True)], [sg.Button('New Employee Add', key='ADD')], 
          [sg.Button('Remove Employee', key='REM')], [sg.Button('Total Today', key='totalButton')]]

window = sg.Window('Clock!', layout)


# and here are the time vars
rightNow = datetime.datetime.now()
theTime = rightNow.strftime("%H:%M:%S")
theDate = rightNow.strftime("%Y-%m-%d")

# def tick():
#     global time = time1
#     time2 = time.strftime('%H:%M:%S')
#     if time2 != time1:
#         time1 = time2
#         window['clock'].Update(time2)
#     time.sleep(0.2)


while True :
#tick()
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
        totalqueery = sg.popup_get_text('who we lookin for')
        whatisit = be.onTheDay(totalqueery, theDate)
        print(whatisit)

    else:
        sg.popup_error(title='I AM CONFUSED')


        
window.Close() 

# here are the csv reader vars
csvItself = open('everyone-master.csv', "r")
parsedcsv = csv.reader(csvItself)

# and here are the time vars
rightNow = datetime.datetime.now()
thisInstant = rightNow.strftime("%H:%M:%S")
justToday = rightNow.strftime("%Y-%m-%d")

# this will take the parsed .csv above, compare the input number, and grab the name associated to it
# so that it may append a document with the name of the numerical date with "Name, Timestamp"
# it then clears the input 
def theThing(): 
      for row in parsedcsv:
          # if current row's 1st value is equal to input, print that row
          if cardNumber == row[0]:
              window.Element('theName').Update(row[1])
              window.Element('theTime').Update(thisInstant)
              window.Element('IN').Update('')
              with open('%s.csv' % justToday, 'a+') as f:
                f.write(f'{row[1]},{thisInstant}\n')

# mainloop:
while True :
      event, value = window.Read()
      cardNumber = value['IN']
      if event is None:
        break 
      elif event is 'RETURN':
            theThing()
      else:
            print('whats going on here')
        
window.Close() 
