from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
from random import *  
import smtplib
from flask_mail import Mail
# from dotenv import load_dotenv
import os
import bcrypt 
from flask_bcrypt import bcrypt

import hashlib
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# app= bcrypt(app) 

# mail = Mail(app)  

# app.config["MAIL_SERVER"]='smtp.gmail.com'  
# app.config["MAIL_PORT"] = 465      
# app.config["MAIL_USERNAME"] = os.environ.get('mail_username')
# app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
# app.config['MAIL_USE_TLS'] = False  
# app.config['MAIL_USE_SSL'] = True  
# mail = Mail(app)  
app.secret_key = 'cairocoders-ednal'

conn = psycopg2.connect(
             database= os.getenv('db_name'), user=os.getenv('db_user'), password=os.getenv('db_password'), host=os.getenv('db_host'), port= os.getenv('db_port')
             )

otp = randint(100000,999999) 

cur = conn.cursor()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    cur = conn.cursor()
    if request.method == "POST":
        fname= request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        passwd = request.form['password']
        c_passwd = request.form['confirm_passsword']
        print(fname, lname, email, passwd, type(c_passwd))
        create_table = ''' CREATE TABLE IF NOT EXISTS UserDetails (
                          fname varchar(40) NOT NULL,
                          lname varchar(40) NOT NULL,
                          passwd varchar(255) NOT NULL,
                          email varchar(40) NOT NULL); '''
        cur.execute(create_table)
        #check for validations pls
        print('table creating')
        #Encryption 
        salt = os.getenv('salt')
        pw= passwd.encode('utf-8')
        print(salt, type(salt), type(pw))
        if passwd==c_passwd:
            key = hashlib.pbkdf2_hmac(
                'sha256', # The hash digest algorithm for HMAC
                pw, # Convert the password to bytes
                salt.encode('utf-8'), # Provide the salt
                100000 # It is recommended to use at least 100,000 iterations of SHA-256 
            )
            cur.execute('INSERT INTO userdetails (fname,lname,passwd,email) VALUES (%s,%s,%s,%s)',(fname,lname,key,email))
            conn.commit()
            return render_template('questions.html')
        else:
            flash('Password does not match')
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return render_template('questions.html')

@app.route('/questions', methods=['GET','POST'])
def questions():
    ques_dic = {1: 'what is the name of your favorite pet?',
                2: 'what is your favorite food?',
                3: 'what was the name of your first elementary school?'}
    print('question test')
    print(ques_dic.get('1'))
    if request.method == 'POST' and 'ans1' in request.form and 'ans2' in request.form and 'ans3' in request.form and 'email' in request.form:
        print('test')
         
        ans1 = request.form['ans1']
        ans2 = request.form['ans2']
        ans3 = request.form['ans3']
        email = request.form['email']
        print(ans1,ans2,ans3,email)
        # create_table_ques = ''' CREATE TABLE IF NOT EXISTS UserQuestions (
        #                   email varchar(40) PRIMARY KEY, 
        #                   q1 varchar(255) NOT NULL,
        #                   q2 varchar(255) NOT NULL,
        #                   q3 varchar(255) NOT NULL,
        #                   ans1 varchar(40) NOT NULL,
        #                   ans2 varchar(40) NOT NULL,
        #                   ans3 varchar(40) NOT NULL); '''
        # cur.execute(create_table_ques)
        # print('table for questions created')
        cur.execute('INSERT INTO userquestions (email,q1,q2,q3,ans1,ans2,ans3) VALUES (%s,%s,%s,%s,%s,%s,%s)',(email,ques_dic[1],ques_dic[2],ques_dic[3],ans1,ans2,ans3))
        print('data entered in userquestions successfully')
        conn.commit()
        return render_template('login.html')

    return render_template('questions.html')

@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == "POST" and 'email' in request.form and 'password' in request.form and 'ans1' in request.form and 'ans2' in request.form and 'ans3' in request.form:
        email = request.form['email']
        passwd = request.form['password']
        ans1 = request.form['ans1']
        ans2 = request.form['ans2']
        ans3 = request.form['ans3']
        #Encryption 
        salt = os.getenv('salt')
        passwdgot = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            passwd.encode('utf-8'), # Convert the password to bytes
            salt.encode('utf-8'), # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        user_details = cur.execute('select * from UserDetails WHERE email = %s', (email,))
        user_answers = cur.execute('SELECT * FROM UserQuestions WHERE email = %s', (email,))
        print(user_details)
        print(user_answers)
        cur.execute('SELECT passwd FROM UserDetails WHERE email = %s', (email,))
        accnt = cur.fetchone()
        cur.execute('SELECT ans1 FROM UserQuestions WHERE email = %s', (email,))
        ans1got = cur.fetchone()
        cur.execute('SELECT ans2 FROM UserQuestions WHERE email = %s', (email,))
        ans2got = cur.fetchone()
        cur.execute('SELECT ans3 FROM UserQuestions WHERE email = %s', (email,))
        ans3got = cur.fetchone()
        print(email,passwd)
        print(accnt[0])
        if accnt:
            passwdreal = accnt[0]
            print(passwdreal)
            if passwdgot == passwdreal and ans1==ans1got and ans2==ans2got and ans3==ans3got:
               return render_template('verify.html', email=-email)
            else:
                flash('Incorrect Username/password')
        else:
            flash('Incorrect Username/password')
        return render_template('verify.html', email=email)
    print('login didnt worked')
    return render_template('verify.html',email=email)
    

@app.route('/verify',methods = ["POST"])  
def verify():
   email = request.form["email"]
   s = smtplib.SMTP('smtp.gmail.com' , 587)
   s.starttls()
   s.login(os.getenv('mail_username') , os.getenv('mail_password'))
   message = str(otp)
   s.sendmail(os.getenv('mail_username') , email , message)
   s.quit()

   return render_template('validate.html') 

@app.route('/validate',methods=["POST"]) 
def validate():
   print(request.form)
   user_otp = request.form['otp']
   if otp == int(user_otp):
     return render_template('home.html')
   
   return render_template('verify.html')   

@app.route("/")
def hello_world():
    return render_template('index.html')
