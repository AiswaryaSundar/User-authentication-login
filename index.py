from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('register.html')

@app.route("/register", methods=['post'])
def register():
    username = request.form["form3Example3"]
    print (username)

def insert_values(self, ques):
        cursor= self.conn.cursor()
        insert_query= "INSERT into employee(name, state) VALUES (%s, %s, %s, %d)"
        cursor.execute(insert_query, data) 
        self.conn.close()    