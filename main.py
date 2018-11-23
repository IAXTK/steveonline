from bs4 import BeautifulSoup
import urllib.request # to fetch the site from the server
import os, time, datetime, random
import glob

import instachat # little module thingy for instagram functions

VERSION = "1.0.1"
SITEURL = "https://sites.google.com/site/facehighschool455" #remote site
WAIT = 120 # seconds to wait btwn checks
LOGFILE = "./steveonline_lg.log"
LOGGING = True


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
        self.name = name # string
        self.hand_in = hand_in # bool
        self.grade = grade # int

    def __str__(self):
        return str(self.name)

classes = { # which <ol> is what class
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
            return assignment.name #this will retn the first

def logThis(message):
    if LOGGING:
        with open(LOGFILE, 'r+') as log:
            log_content = log.read()
            entry = "LOG." + str(datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")) + ": " + message + "\n"
            log.seek(0,0)
            log.write(entry + log_content)

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
        print("Error! Wtf! Server is down/You disconnected! Skipping.")
        logThis("Error! Wtf! Server is down/You disconnected! Skipping.")
        return 1234
    isSame = -1
    assignmentsForRealtime = generateAssignments(realtime_file)
    assignmentsForLatest = generateAssignments(latest_file)

    for i in range(len(generateAssignments(realtime_file))):
        if assignmentsForRealtime[i].name == assignmentsForLatest[i].name:
            isSame = 1
        else:
            isSame = 0
            break
    if isSame and len(assignmentsForRealtime) == len(assignmentsForLatest): #true: same
        print("Site is same, skipping")
        logThis("site is same. skipping.")
    else:
        print("Found different!!")
        logThis("Found different!!")
        initializeArchive() # add new site version to archive
        instachat.sendMessage("New assignment for " + classes[2] + "! \n" + findLatestAssignment(assignmentsForRealtime, 2), instachat.getPeople() )
        logThis("SENT! 'New assignment for " + classes[2] + "! " + findLatestAssignment(assignmentsForRealtime, 2) + "to " + str(len(instachat.getPeople())) + " people!")

if __name__ == '__main__':
    logThis("Program start! Version " + VERSION)
    if not os.listdir("archives/"): #aka empty
        print("First run or flushed, initializing archive.")
        initializeArchive()

    while 1:
        print("Running main checker..")
        startTime = datetime.datetime.now()
        mainThing()
        print("done checker in "+ str(datetime.datetime.now()-startTime))
        logThis("done checker in " + str(datetime.datetime.now()-startTime))
        print("Waiting for cycle...")
        time.sleep(WAIT)
        print("Done wait!")

