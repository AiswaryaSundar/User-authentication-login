from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('register.html')

@app.route("/register", methods=['post'])
def register():
    username = request.form["form3Example3"]
    print (username)