from bs4 import BeautifulSoup
from tkinter import filedialog
from datetime import datetime, timedelta

# config
last = 15  # number of weeks last a semester
remind = 15  # remind number of minutes ahead
firstDayClass = "20210906T000000"  # first day of class

# init
form = '%Y%m%dT%H%M%S'
startDate = datetime.strptime(firstDayClass, form)
endDate = startDate + timedelta(weeks=last, days=-1)
switch = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}


def addCourse(file, title, loca, byDay, time):
    dateTimeStart = startDate + timedelta(days=byDay-1,
                                          hours=int(time[0].split(':')[0]),
                                          minutes=int(time[0].split(':')[1]))
    dateTimeEnd = startDate + timedelta(days=byDay-1,
                                        hours=int(time[1].split(':')[0]),
                                        minutes=int(time[1].split(':')[1]))
    dateTimeStart = datetime.strftime(dateTimeStart, form)
    dateTimeEnd = datetime.strftime(dateTimeEnd, form)
    file.write("BEGIN:VEVENT\nSUMMARY:" + title + "\nLOCATION:" + loca
               + "\nDTSTART;TZID=China Standard Time:" + dateTimeStart
               + "\nDTEND;TZID=China Standard Time:" + dateTimeEnd
               + "\nRRULE:FREQ=WEEKLY;UNTIL=" +
               datetime.strftime(endDate, form)
               + "Z;INTERVAL=1;BYDAY=" + switch[byDay]
               + "\nBEGIN:VALARM\nACTION:DISPLAY\nDESCRIPTION:REMINDER\nTRIGGER:-PT"
               + str(remind) + "M\nEND:VALARM\nEND:VEVENT\n")


# open htmlfile
path = filedialog.askopenfilename(title="", filetypes=[
    ("html files", "*.html"), ("html files", "*.htm")])
htmlfile = open(path, 'r', encoding='utf-8')

# create ics file
path = filedialog.asksaveasfilename(
    title="", filetypes=[("ics files", ".ics")])
if (path == ""):
    exit()

# write head
file = open(path.split(".")[0]+'.ics', 'w')
file.write('''BEGIN:VCALENDAR
PRODID:UIC timetable
VERSION:2.0
''')

# make soup
soup = BeautifulSoup(htmlfile, 'html.parser').find(id="mytimetable")
tr = soup.find_all("tr")
del tr[0]  # remove head of table

for row in tr:
    for byDay, col in enumerate(row.find_all("td"), 1):
        strings = list(col.stripped_strings)  # remove space and split
        if (len(strings) != 0):
            addCourse(file, strings[0], strings[1],
                      byDay, row.th.string.split('-'))

file.write("END:VCALENDAR")
file.close()
