import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#create a user table 

# First name, last name, email, mobile, ques1, ques2, ques3, hint1, hint2, hint3, ans1, ans2, ans3

#insert values
