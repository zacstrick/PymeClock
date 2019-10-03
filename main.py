import csv
import sys
import datetime
import pandas as pd
import numpy as np
import openpyxl as xl

loopty = True
def prog() :
      
# input number you want to search
  cardNumber = input('Ready for your swipe!\n')

# here are the csv reader vars
  csvItself = open('everyone-master.csv', "r")
  parsedcsv = csv.reader(csvItself)
  
# this'll be the csv writer's vars
  #newCSV = open("C:\Users\zstrickland.RANDSMACHINE\Documents\ClockInCardProject\ClockInPython\eweveryone.csv")
  #writer = csv.writer(newCSV)

# and here are the time vars
  rightNow = datetime.datetime.now()
  thisInstant = rightNow.strftime("%Y-%m-%d %H:%M:%S")

# This one displays the username and date/time of clockin
# loop through csv list
  for row in parsedcsv:
    # if current row's 1st value is equal to input, print that row
      if cardNumber == row[0]:
          print(row[1])
          print(thisInstant)
      


# here's how to find the row of the given card number
  def row_number(input):
      o = open('everyone-master.csv', 'r') 
      myData = csv.reader(o)
      index = 0 
      for row in myData:
      #print row
       if row[0] == input: 
          return index 
       else : index += 1
  userRowNumber = row_number(cardNumber)
  print(userRowNumber)
while loopty :
  prog()