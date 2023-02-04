from flask import Flask
import random

app = Flask(__name__)

def get_questions(): 
    # fucn to api
    # ques = ["what is the name of your favorite pet?", "what is your favorite food?", "what was the name of your first elementary school?","what is your birth city?", "what high school did you attend?" ]

    ques_dic = {1: 'what is the name of your favorite pet?', 2: 'what is your favorite food?', 3: 'what was the name of your first elementary school?', 4: 'what is your birth city?', 5: 'what high school did you attend?'}
    ans=[]

    for i in range(3):
        rand_ques = random.choice(list(ques_dic.values()))
        ans.append(rand_ques)

    return ans 


def receive_ans(ans):
    # function to store answer and hint 
    ans_dic= {}
    list_ans=[]
    for i in range(len(ans)):
        ans1 = input()
        hint = input()

        list_ans.append(ans1)
        list_ans.append(hint)

        ans_dic[ans[i]]=list_ans

    return ans_dic



@app.route("/")
def hello_world():
    return "<p>Hello, World! rahul</p>"
