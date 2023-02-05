
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras

hostname = '127.0.0.1'
database = 'postgres'
username = 'postgres'
pwd = 'Aruba@123'
port_id = 5433
#conn = None
#cur = None

# try:
#     conn = psycopg2.connect(
#              host='localhost', 
#              database='postgres',
#              user='postgres',
#              password='Aruba@123',
#              port='5433'
#              )

#     cur = conn.cursor()

#     create_table = ''' CREATE TABLE IF NOT EXISTS users (
#                          id  int PRIMARY KEY,
#                          fname varchar(40) NOT NULL,
#                          lname varchar(40) NOT NULL,
#                          uname varchar(40) NOT NULL,
#                          email varchar(40) NOT NULL); '''

#     create_table_ques = ''' CREATE TABLE IF NOT EXISTS UserQuestions (
#                          CONSTRAINT fk_Email  
#                          FOREIGN KEY(email)   
#                          REFERENCES UsersDetails(email)
#                          q1 varchar(40) NOT NULL,
#                          q2 varchar(40) NOT NULL,
#                          q3 varchar(40) NOT NULL,
#                          ans1 varchar(40) NOT NULL,
#                          ans2 varchar(40) NOT NULL,
#                          ans3 varchar(40) NOT NULL); '''
#     cur.execute(create_table)

#     conn.commit()
# except Exception as error:
#     print('DB Connection Error')
# finally:
#     if cur is not None:
#      cur.close()
#     if conn is not None: 
#      conn.close()

conn = psycopg2.connect(
             host='localhost', 
             database='demodb',
             user='postgres',
             password='Aruba@123',
             port='5433'
             )

cur = conn.cursor()



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST' and 'fname' in request.form and 'passwd' in request.form and 'lname' in request.form and 'email' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        passwd = request.form['password']
        print(email,fname)
        create_table = ''' CREATE TABLE IF NOT EXISTS users (
                          fname varchar(40) NOT NULL,
                          lname varchar(40) NOT NULL,
                          passwd varchar(40) NOT NULL,
                          email varchar(40) NOT NULL); '''
        #check for validations pls

        cur.execute('INSERT INTO UsersDetails (fname,lname,passwd,email) VALUES (%s,%s,%s,%s)',(fname,lname,passwd,email))
        conn.commit()
    elif request.method == 'POST' :
        flash('Please fill out the form !')


    return render_template('questions.html')

@app.route('/questions', methods=['GET','POST'])
def questions():
    ques_dic = {1: 'what is the name of your favorite pet?',
                2: 'what is your favorite food?',
                3: 'what was the name of your first elementary school?'}
    if request.method == 'POST' and 'ans1' in request.form and 'ans2' in request.form and 'ans3' in request.form and 'email' in request.form:
        ans1 = request.form['ans1']
        ans2 = request.form['ans2']
        ans3 = request.form['ans3']
        email = request.form['email']
        print(ans1,ans2)

        cur.execute('INSERT INTO UsersQuestions (email,ans1,ans2,ans3) VALUES (%s,%s,%s,%s)',(email,ans1,ans2,ans3))
        conn.commit()
    elif request.method == 'POST' :
        flash('Please fill out the form !')

    return render_template('login.html')

@app.route('/login/', methods=['GET','POST'])
def login():

    if request.method == 'POST' and 'email' in request.form and 'passwd' in request.form:
        email = request.form['email']
        passwd = request.form['passwd']
        print(passwd)
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        accnt = cur.fetchone()

        if accnt:
            passwdreal = accnt['passwd']
            print(passwdreal)
            if passwd == passwdreal:
               return redirect(url_for('home'))
            else:
                flash('Incorrect Username/password')
        else:
            flash('Incorrect Username/password')

    return render_template('login.html')





# from flask import Flask, render_template, request
# import psycopg2


# app = Flask(__name__)

# @app.route("/security_question_validation")
# def get_questions(): 
#     # function to api
#     try: 
#         conn = psycopg2.connect(database="demo", host='127.0.0.1', port= '5432')
#     except:
#         print("DB not connected")
#     conn.autocommit = True
#     cursor = conn.cursor()
#     a1="rosi"
#     a2="roti"
#     a3="kns"
#     r1=request.form['q1']
#     r2=request.form['q2']
#     r3=request.form['q3']
#     if(r1==a1 and r2==a2 and r3==a3):
#         return "<h2>Login Success</h2>"
#     else:
#         return render_template("/")

# @app.route("/")
# def hello_world():
#     ques_dic = {1: 'what is the name of your favorite pet?',
#                 2: 'what is your favorite food?',
#                 3: 'what was the name of your first elementary school?'}
#     return render_template('index.html',ques=ques_dic)
