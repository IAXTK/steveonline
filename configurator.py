# SteveOnline Account Configurator
# Run to set credentials.

cred_file = open("./credentials.txt", 'w')
username = input("Username>> ")
password = input("Password>> ")
print("Setting... {} :: {}".format(username,password))
cred_file.write("{}\n{}".format(username, password))
print("done!")
cred_file.close()