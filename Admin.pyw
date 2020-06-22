import PySimpleGUI as sg
import TimeclockBE as be
import datetime
import week
import os.path

def write_to_csv(listoftimes, sow, eow):
    with open(f'records/{sow} to {eow}.csv', 'w+') as csvfile:
        for domain in listoftimes:
            csvfile.write(domain + '\n')


layout = [[sg.Text('Timeclock Admin Portal', font=('arial', 18, 'bold'))], 
         [sg.Button("Currently on the Clock", key='OTC')], [sg.Button('Vacation Requests', key='VAC')], 
         [sg.Button("Specific Week's Times", key='TWT')], [sg.Button("IIIIIIIT'S MONDAY", key='LWT')]]

window = sg.Window('Admin Center', layout)

while True:
    event, value = window.Read(timeout=1000)
    
    rightNow = datetime.datetime.now()
    theTime = rightNow.strftime("%H:%M:%S")
    theDate = rightNow.strftime("%Y-%m-%d")

    if event == None:
        break

    if event == 'OTC':
        current = be.inCurrently(theDate)
        print(current)
    
    elif event == 'LWT':
        tooday = datetime.date.today()
        sow = tooday - datetime.timedelta(days=tooday.weekday()+7)
        eow = sow + datetime.timedelta(days=6)
        print(sow)
        print(eow)
        whichdb = be.database
        times = week.OTW(str(sow), str(eow), whichdb)
        write_to_csv(times, sow, eow)
        sg.popup('A list of times has been created in the PymeClock folder titled "{} to {}"'.format(sow, eow))

    #elif event == 'VAC':

    elif event == 'TWT':
        whichdb = sg.popup_get_text('Which Database would you like to use?\nEnter the full path with no quotes:', default_text='Z:/.db')
        pathcheck = os.path.exists(whichdb)
        print(whichdb)
        print(pathcheck)

        if whichdb == None:
            sg.popup('um I need a database to look through.')
            pass

        if pathcheck == False:
            sg.popup("sorry, that's not a valid path.")
            pass

        else:
            sow = sg.popup_get_text('Where did the week begin? YYYY-MM-DD')

            if sow == '' or None:
                sg.popup('I need a starting date to run the query')
            else:
                eow = sg.popup_get_text('Where did the week end? YYYY-MM-DD')
                if eow == '' or None:
                    sg.popup('I need both times in order to work')
                else:

                    times = week.OTW(sow, eow, whichdb)
                    write_to_csv(times, sow, eow)
                    sg.popup('A list of times has been created in the PymeClock folder under "records" titled "{} to {}"'.format(sow, eow))
    


window.Close()