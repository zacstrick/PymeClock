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

window = sg.Window('Clock!', layout)

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
