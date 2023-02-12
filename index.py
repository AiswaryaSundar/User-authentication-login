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
from createTable import Table
import hashlib

app = Flask(__name__)
# app= bcrypt(app) 

mail = Mail(app)  

app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = os.environ.get('mail_username')
app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
app.secret_key = 'cairocoders-ednal'
obj= Table() 
# obj.create_table()
# obj.create_security_table()
obj.add_security_data() 
obj.add_question_data()

conn = psycopg2.connect(
             database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
             )

otp = randint(100000,999999) 

cur = conn.cursor()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname= request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        passwd = request.form['password']
        c_passwd = request.form['confirm_passsword']
        print(fname, lname, email, passwd, c_passwd)
        
        #Encryption 
        salt = os.urandom(32) # Remember this
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            passwd.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        confirm_key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            c_passwd.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        if key== confirm_key:
            print("Inserted values")
            obj.insert_values([fname, lname, key, email])
            return render_template('success.html')
        else:
            flash('Password does not match')

    return render_template('register.html')

@app.route('/questions', methods=['GET','POST'])
def questions():
    ques_dic = {1: 'what is the name of your favorite pet?',
                2: 'what is your favorite food?',
                3: 'what was the name of your first elementary school?'}
    if request.method == 'POST' and 'ans1' in request.form and 'ans2' in request.form \
        and 'ans3' in request.form and 'email' in request.form:
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
               return render_template('verify.html', email = email)
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
