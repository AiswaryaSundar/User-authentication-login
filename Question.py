# from flask import Flask

# app = Flask(__name__)

# @app.route("/")


ques = ["what is the name of your favorite pet?", "what is your favorite food?", "what was the name of your first elementary school?","what is your birth city?", "what high school did you attend?" ]

ques_dic = {1: 'what is the name of your favorite pet?', 2: 'what is your favorite food?', 3: 'what was the name of your first elementary school?', 4: 'what is your birth city?', 5: 'what high school did you attend?'}

print("what is the name of your favorite pet?")
ans1=input()
hint1 = input()
print("what is your favorite food?")
ans2=input()
hint2 = input()
print("what was the name of your first elementary school?")
ans3=input()
hint3 = input()
print("what is your birth city?")
ans4=input()
hint4 = input()
print("what high school did you attend?")
ans5=input()
hint5 = input()



# def askUser():
#     username = input("Enter your username: ")
#     password = input("Enter your password: ")
#     checkPass(username, password)

# def checkPass(use, pwd):
#     if use == "username" and pwd == "password":
#         login(use)
#     else:
#         print "Your username and/or password was incorrect"
#         askUser()

# def login(use):
#     print "Welcome " + use
#     print "You have successfully logged in!"
#     askCom()

# def askCom():
#     command = raw_input("Enter your command: ")
#     if command == "log off" or command == "quit":
#         username = ""
#         password = ""
#         print "You have logged off"
#         askUser()
#     else:
#         print "Unknown command"
#         askCom()

# askUser()