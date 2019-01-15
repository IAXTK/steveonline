from InstagramAPI import InstagramAPI
import story3 # yay finally back
import hashlib

class LoginError(Exception):
    pass

def sendMessage(message, recipients):
    #get credentials from file!
    user_name = open("./credentials.txt", "r").readlines()[0]
    password = open("./credentials.txt", "r").readlines()[1]

    api = InstagramAPI(user_name, password)
    if (api.login()):
        pass
    else:
        raise LoginError("Cannot login!")

    #text = "Hello there!"
    for username in recipients:
        api.searchUsername(username)
        response = api.LastJson
        print("sending to " + username)
        api.direct_message(message, response['user']['pk'])
    print("done sending!")
    return 0

def makeStory(message):
    #get credentials from file!
    user_name = open("./credentials.txt", "r").readlines()[0]
    password = open("./credentials.txt", "r").readlines()[1]

    api = InstagramAPI(user_name, password)
    if (api.login()):
        pass
    else:
        raise LoginError("Cannot login!")
    filename = "./stories/" + hashlib.sha224(message).hexdigest() + ".jpg"
    story3.makeStory(message, filename)
    InstagramAPI.uploadStoryPhoto(api, filename)

def getPeople():
    #get credentials from file!
    user_name = open("./credentials.txt", "r").readlines()[0]
    password = open("./credentials.txt", "r").readlines()[1]

    api = InstagramAPI(user_name, password)
    if (api.login()):
        pass
    else:
        raise LoginError("Cannot login!")

    followers = api.getTotalSelfFollowers()
    followersByUsername = [] # this just makes the logs look nicer
    for follower in followers:
        followersByUsername.append(follower['username'])
    return followersByUsername