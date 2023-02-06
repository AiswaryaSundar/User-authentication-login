from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
from random import *  
import smtplib
from flask_mail import Mail
from dotenv import load_dotenv
import os

app = Flask(__name__)
mail = Mail(app)  

app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = os.environ.get('mail_username')
app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
app.secret_key = 'cairocoders-ednal'

conn = psycopg2.connect(
             host='localhost', 
             database='demo',
             port='5432',
             user='postgres',
             password='gokul1234'
             )

otp = randint(100000,999999) 

cur = conn.cursor()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['GET','POST'])
def register():
    cur = conn.cursor
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        lname = request.form['lname']
        email = request.form['email']
        passwd = request.form['password']
        c_passwd = request.form['confirm_passsword']
        create_table = ''' CREATE TABLE IF NOT EXISTS users (
                          fname varchar(40) NOT NULL,
                          lname varchar(40) NOT NULL,
                          passwd varchar(40) NOT NULL,
                          email varchar(40) NOT NULL); '''
        #check for validations pls
        print('table creating')
        create_table_ques = ''' CREATE TABLE IF NOT EXISTS UserQuestions (
                          CONSTRAINT fk_Email  
                          FOREIGN KEY(email)   
                          REFERENCES users(email)
                          q1 varchar(40) NOT NULL,
                          q2 varchar(40) NOT NULL,
                          q3 varchar(40) NOT NULL,
                          ans1 varchar(40) NOT NULL,
                          ans2 varchar(40) NOT NULL,
                          ans3 varchar(40) NOT NULL); '''
        cur.execute(create_table)
        cur.execute(create_table_ques)
        if passwd==c_passwd:
            cur.execute('INSERT INTO users (fname,lname,passwd,email) VALUES (%s,%s,%s,%s)',(fname,lname,passwd,email))
            conn.commit()
            return render_template('questions.html')
        else:
            flash('Password does not match')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('register.html')

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

        cur.execute('INSERT INTO users (email,ans1,ans2,ans3) VALUES (%s,%s,%s,%s)',(email,ans1,ans2,ans3))
        conn.commit()
        return render_template('login.html')

    return render_template('questions.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'passwd' in request.form:
        email = request.form['email']
        passwd = request.form['passwd']
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        accnt = cur.fetchone()

        if accnt:
            passwdreal = accnt['passwd']
            print(passwdreal)
            if passwd == passwdreal:
               return render_template('home.html')
            else:
                flash('Incorrect Username/password')
        else:
            flash('Incorrect Username/password')
    return render_template('index.html')

@app.route('/verify',methods = ["POST"])  
def verify():
   email = request.form["email"]
   s = smtplib.SMTP('smtp.gmail.com' , 587)
   s.starttls()
   s.login(os.environ.mail_username   , os.environ.mail_password)
   message = str(otp)
   s.sendmail(os.environ.mail_username , email , message)
   s.quit()
   return render_template('verify.html') 

@app.route('/validate',methods=["POST"]) 
def validate():
   user_otp = request.form['otp']
   if otp == int(user_otp):
     return "<h3> Email  verification is  successful </h3>"
   
   return "<h3>failure, OTP does not match</h3>"   

@app.route("/")
def hello_world():
    return render_template('index.html')
