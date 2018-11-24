from bs4 import BeautifulSoup
import urllib.request # to fetch the site from the server
import os, time, datetime, random
import glob

import instachat # little module thingy for instagram functions

VERSION = "1.0.2" #pretty much meaningless?
SITEURL = "https://sites.google.com/site/facehighschool455" #remote site
WAIT = 120 # seconds to wait btwn checks
LOGFILE = "./steveonline_lg.log"
LOGGING = True
ENABLED_GRADES = [2,3]
FLUSH_EVERY = -1 #flush the archives 

def fetch_latest():
    page = urllib.request.urlopen(SITEURL)
    return str(page.read(), 'utf-8')

def compare_versions(old, new):
    if hash(old) == hash(new): #compare
        return True
    else:
        return False


class Assignment(object):
    def __init__(self, name, hand_in, grade):
        self.name = name # the name of the assignment
        self.hand_in = hand_in # is it hand in? (unused)
        self.grade = grade # the grade that the assignment belongs to

    def __str__(self):
        return str(self.name)

grades = { # which <ol> is what grade
    0: 'Math 9E',
    1: 'Science 9E',
    2: 'Math 8E',
    3: 'Science 8E',
    4: 'Science 7E'
}

def generateAssignments(page):
    soup = BeautifulSoup(page, features='html.parser')
    items = []
    for alist in soup.find_all('ol'):
        for list_item in alist.find_all('li'):
            assignment_bits = list_item.find_all('font')
            assignment_strings = []
            for component in assignment_bits:
                assignment_strings.append(component.text)
            assignment_name_compound = "".join(assignment_strings)
            assignment_grade = soup.find_all('ol').index(alist)
            if "hand in" in assignment_name_compound:
                assignment_is_hand_in = True
            else:
                assignment_is_hand_in = False
            assignment = Assignment(assignment_name_compound, assignment_is_hand_in, assignment_grade)
            items.append(assignment)
    return items

def findLatestAssignment(assignments, grade):
    for assignment in assignments:
        if assignment.grade == grade:
            return assignment.name #this will return the first

def logThis(message):
    if LOGGING:
        with open(LOGFILE, 'r+') as log:
            log_content = log.read()
            entry = "LOG." + str(datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")) + ": " + message + "\n"
            log.seek(0,0)
            log.write(entry + log_content)
    print(message)

def initializeArchive():
    # run only if there is no file in archive
    filename = 'archives/' + str(datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")) + '.sitefile'
    init_file = open(filename, 'w')
    init_file.write(fetch_latest())
    init_file.close()

def makeUserList():
    users = []
    userfile = open("people.txt")
    for line in userfile.readlines():
        userdata = line.split(':')
        users.append(userdata[0])
    return users

def mainThing():
    list_of_files = glob.glob('archives/*.sitefile')
    latest_file = open(max(list_of_files, key=os.path.getctime), 'rb').read()
    try:
        realtime_file = fetch_latest()
    except:
        logThis("Error! Wtf! Server is down/You disconnected! Skipping.")
        return 1234
    assignmentsForRealtime = generateAssignments(realtime_file)
    assignmentsForLatest = generateAssignments(latest_file)

    for grade in ENABLED_GRADES:
        if (findLatestAssignment(assignmentsForRealtime, grade) == findLatestAssignment(assignmentsForLatest, grade) and 
                len(assignmentsForRealtime) == len(assignmentsForLatest) ):
            
            logThis("The site is same, skipping.")
    
        else:
            logThis("Found different!!")
            initializeArchive() # add new site version to archive
            instachat.sendMessage("New assignment for " + grades[grade] + "! \n" + findLatestAssignment(assignmentsForRealtime, grade), instachat.getPeople() )
            logThis("SENT! 'New assignment for " + grades[grade] + "! " + findLatestAssignment(assignmentsForRealtime, grade) + "to " + str(len(instachat.getPeople())) + " people!")

if __name__ == '__main__':
    logThis("Program start! Version " + VERSION)
    logThis("Enabled grades: " + str(ENABLED_GRADES))
    if not os.listdir("archives/"): #aka empty
        logThis("First run or flushed, initializing archive.")
        initializeArchive()

    while 1:
        print("Running main checker..")
        startTime = datetime.datetime.now()
        mainThing()
        logThis("done checker in " + str(datetime.datetime.now()-startTime))
        time.sleep(WAIT)
