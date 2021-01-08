from datetime import datetime, timedelta
import os
import re

firstMonday = datetime.strptime('01/11/2021', "%m/%d/%Y")
classDays = ["Mon", "Wed"]
weeksPath = './sections/weeks'
latexDateCommand = "\placeDate"
markerA = "% replace dates begin"
markerB = "% replace dates end"
calendarString = "\parbox[t]{{\weeksLength}}{{\\textbf{{\\hypertarget{{week{weekNumber}}}Week {weekNumber}}} \\\\ {dates} }} & \week{weekCharacter} \\tend \n"

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

nextMonday = lambda date, weekFromFirst: firstMonday + timedelta(days=((7*weekFromFirst)))

weeks = natural_sort(os.listdir(weeksPath))
dayNames = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]
classDaysIdx = []
calendarItems = []

def findClassDatesIndices():
	for d in classDays:
		classDaysIdx.append(dayNames.index(d))

def updateWeekDates():
	for idx, w in enumerate(weeks):
		m = re.search(r"\d+", w)
		week = int(m.group())
		days = [nextMonday(firstMonday, week-1)]

		for i in range(1, 7):
			days.append(days[0] + timedelta(days=i))

		generatedDates = [d.strftime("\def\d"+dayNames[idx]+"{" +dayNames[idx]+ ", %m/%d}\n") for idx, d in enumerate(days)]
		generatedDates.append(latexDateCommand + "\n")

		path = os.path.join("./sections/weeks", w)
		with open(path) as f:
			lines = f.readlines()

		lastLineToClear = 0
		for num, line in enumerate(lines):
			if latexDateCommand in line:
				lastLineToClear = num+1
		
		lines[:lastLineToClear] = ""
		newFileWithUpdatedDates = generatedDates + lines

		with open(path, "w") as f:
			f.writelines(newFileWithUpdatedDates)

		weekDates = [days[x].strftime("%m/%d") for x in classDaysIdx]
		datesString = "---".join(weekDates)
		calendarItems.append(calendarString.format(weekNumber = idx+1, dates = datesString, weekCharacter=chr(65+idx)))

def updateCalendarFile():
	with open("./sections/calendar.tex") as f:
		lines = f.readlines()

	firstLineToClear = 0
	lastLineToClear = 0

	for num, line in enumerate(lines):
		if markerA in line:
			firstLineToClear = num+1
		if markerB in line:
			lastLineToClear = num

	lines[firstLineToClear:lastLineToClear] = calendarItems

	with open("./sections/calendar.tex", "w") as f:
		f.writelines(lines)


findClassDatesIndices()
updateWeekDates()
updateCalendarFile()