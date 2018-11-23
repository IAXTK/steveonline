from InstagramAPI import InstagramAPI

class LoginError(Exception):
    pass



def sendMessage(message, recipients):
    print("beginning message transmission")
    #get credentials from file!
    user_name = open("./credentials.txt", "r").readlines()[0]
    password = open("./credentials.txt", "r").readlines()[1]

    api = InstagramAPI(user_name, password)
    if (api.login()):
        api.getSelfUserFeed()  # get self user feed
        #print(api.LastJson)  # print last response JSON
        print("Login success!")
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

def getPeople():
    print("getting people..")
    #get credentials from file!
    user_name = open("./credentials.txt", "r").readlines()[0]
    password = open("./credentials.txt", "r").readlines()[1]

    api = InstagramAPI(user_name, password)
    if (api.login()):
        api.getSelfUserFeed()  # get self user feed
        #print(api.LastJson)  # print last response JSON
        print("Login success!")
    else:
        raise LoginError("Cannot login!")

    followers = api.getTotalSelfFollowers()
    realf = []
    for follower in followers:
        realf.append(follower['username'])
    print("done getting people!")
    return realf