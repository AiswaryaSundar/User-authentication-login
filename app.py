from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
from random import *  
import smtplib
from email.message import EmailMessage

import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Flask mail implementation
# app= bcrypt(app) 
# mail = Mail(app)  
# app.config["MAIL_SERVER"]='smtp.gmail.com'  
# app.config["MAIL_PORT"] = 465      
# app.config["MAIL_USERNAME"] = os.environ.get('mail_username')
# app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
# app.config['MAIL_USE_TLS'] = False  
app.secret_key = 'cairocoders-ednal'

global otp

def genrate_otp():
    otp = randint(100000,999999)
    return otp

otp=genrate_otp()

# Database connection 
def connection_object():
    connection = None
    try:
        connection = psycopg2.connect(
             database= os.getenv('db_name'), user=os.getenv('db_user'), password=os.getenv('db_password'), host=os.getenv('db_host'), port= os.getenv('db_port')
             )
    except Exception as e:
        print(e)
    return connection

# Create/Alter Tables with this fuction
def execute_query(connection, query):
    cusor = connection.cursor()
    try:
        cusor.execute(query)
        connection.commit()
    except Exception as e:
        print(e)
        
# Insert/Update the values into the table
def execute_query_with_val(connection, query, val):
    cusor = connection.cursor()
    try:
        cusor.execute(query, val)
        connection.commit()
    except Exception as e:
        print(e)

# Read data from the database and return the result as Tuple
def read_query(connection, query, val):
    cursor = connection.cursor()
    try:
        cursor.execute(query, val)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)    

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    register_connection= connection_object()
    if request.method == "POST":
        fname= request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        passwd = request.form['password']
        c_passwd = request.form['confirm_passsword']
        create_table = ''' CREATE TABLE IF NOT EXISTS user_details (
                          fname varchar(40) NOT NULL,
                          lname varchar(40) NOT NULL,
                          passwd varchar(255) NOT NULL,
                          email varchar(40) NOT NULL); '''
        execute_query(register_connection, create_table) #Creating User Details Table
        #Encryption 
        if passwd==c_passwd:
            key = hashlib.pbkdf2_hmac(
                'sha256', # The hash digest algorithm for HMAC
                passwd.encode('utf-8'), # Convert the password to bytes
                os.getenv('salt').encode('utf-8'), # Provide the salt
                100000 # It is recommended to use at least 100,000 iterations of SHA-256 
            )
            #Insering usser details into table
            execute_query_with_val(register_connection,'INSERT INTO user_details (fname,lname,passwd,email) VALUES (%s,%s,%s,%s)',(fname,lname,key,email))
            register_connection.commit() #Saving the DB changes
            register_connection.close() #Closing the DB Connection
            return render_template('questions.html', email=email)
        else:
            flash('Password does not match')
    return render_template('register.html')

@app.route('/questions', methods=['GET','POST'])
def questions():
    questions_connection = connection_object()
    ques_dic = {1: 'what is the name of your favorite pet?',
                2: 'what is your favorite food?',
                3: 'what was the name of your first elementary school?'}
    if request.method == 'POST' and 'ans1' in request.form and 'ans2' in request.form and 'ans3' in request.form and 'email' in request.form:
        print('test')
         
        ans1 = request.form['ans1']
        ans2 = request.form['ans2']
        ans3 = request.form['ans3']
        email = request.form['email']
        print(ans1,ans2,ans3,email)
        create_table_ques = ''' CREATE TABLE IF NOT EXISTS user_questions (
                          email varchar(40) PRIMARY KEY, 
                          q1 varchar(255) NOT NULL,
                          q2 varchar(255) NOT NULL,
                          q3 varchar(255) NOT NULL,
                          ans1 varchar(40) NOT NULL,
                          ans2 varchar(40) NOT NULL,
                          ans3 varchar(40) NOT NULL); '''
        execute_query(questions_connection,create_table_ques) # Creating User Questions Table
        print('table for questions created')
        execute_query_with_val(questions_connection,'INSERT INTO user_questions (email,q1,q2,q3,ans1,ans2,ans3) VALUES (%s,%s,%s,%s,%s,%s,%s)',(email,ques_dic[1],ques_dic[2],ques_dic[3],ans1,ans2,ans3))
        print('data entered in userquestions successfully')
        questions_connection.commit()
        questions_connection.close()
        return render_template('login.html')

    return render_template('questions.html')

@app.route('/login', methods=['GET','POST'])
def login():
    login_connection = connection_object()
    if request.method == "POST" and 'email' in request.form and 'password' in request.form and 'ans1' in request.form and 'ans2' in request.form and 'ans3' in request.form:
        email = request.form['email']
        passwd = request.form['password']
        ans1 = request.form['ans1']
        ans2 = request.form['ans2']
        ans3 = request.form['ans3']
        #Encryption 
        passwdgot = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            passwd.encode('utf-8'), # Convert the password to bytes
            os.getenv('salt').encode('utf-8'), # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        user_details = read_query(login_connection,'SELECT * FROM user_details WHERE email = %s', (email,)) # Reading user details
        user_answers = read_query(login_connection,'SELECT * FROM user_questions WHERE email = %s', (email,)) # Reading uset answers
        
        if True:
            passwdreal = list(user_details[2])
            # print(passwdreal, user_details[2])
            if passwdgot == passwdreal and ans1==user_answers[5] and ans2==user_answers[6] and ans3==user_answers[7]:
               return render_template('verify.html', email=email)
            else:
                flash('Incorrect Username/password')
        # else:
            flash('Incorrect Username/password')
        return render_template('verify.html', email=email)
    print('login didnt worked')
    return render_template('login.html',email=email)
    

@app.route('/verify',methods = ["POST"])  
def verify():
   genrate_otp()
#    print(otp)
   email = request.form["email"]
   print(email)
   s = smtplib.SMTP('smtp.gmail.com' , 587)
   s.starttls()
   msg = EmailMessage()
   msg['Subject'] = 'OTP for authentication'
   msg['From'] = os.getenv('mail_username')
   msg['To'] = email
   msg.set_content('This is the OTP for 3-Factor Verification of your account:'+str(otp)+'\nPlease do not share this OTP with anyone.')
   s.login(os.getenv('mail_username') , os.getenv('mail_password'))
   s.send_message(msg) #Sending OTP to the email
   s.quit()
   return render_template('validate.html') 

@app.route('/validate',methods=["POST"]) 
def validate():
   print(request.form)
   user_otp = request.form['otp']
   if otp == int(user_otp): # Validating the OTP entered by the User
     return render_template('home.html')
   
   return render_template('verify.html')   

@app.route("/")
def hello_world():
    return render_template('index.html')
