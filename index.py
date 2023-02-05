from flask import Flask, render_template, request
import psycopg2


app = Flask(__name__)

@app.route("/security_question_validation")
def get_questions(): 
    # function to api
    try: 
        conn = psycopg2.connect(database="demo", host='127.0.0.1', port= '5432')
    except:
        print("DB not connected")
    conn.autocommit = True
    cursor = conn.cursor()
    a1="rosi"
    a2="roti"
    a3="kns"
    r1=request.form['q1']
    r2=request.form['q2']
    r3=request.form['q3']
    if(r1==a1 and r2==a2 and r3==a3):
        return "<h2>Login Success</h2>"
    else:
        return render_template("/")

@app.route("/")
def hello_world():
    ques_dic = {1: 'what is the name of your favorite pet?', 2: 'what is your favorite food?', 3: 'what was the name of your first elementary school?'}
    return render_template('index.html',ques=ques_dic)
