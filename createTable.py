import psycopg2

from Question import ques_dic
class Table():
    def create_security_table(self): 
        self.conn = psycopg2.connect(
        database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
        )
        self.conn.autocommit = True
        cursor = self.conn.cursor()
        initial_check="DROP TABLE IF EXISTS securitydata; DROP TABLE IF EXISTS questiondata;"
        question_data= "create table questiondata (qid integer PRIMARY KEY, question varchar(256));"
        user_security_data = "create table securitydata (email varchar(256) PRIMARY KEY, ques1 integer, ques2 integer, ques3 integer, ans1 varchar(256), \
        ans2 varchar(256), ans3 varchar(256), hint1 varchar(256), hint2 varchar(256), hint3 varchar(256));"
        # Create a table in PostgreSQL database
        cursor.execute(initial_check)
        cursor.execute(question_data)
        cursor.execute(user_security_data)
        self.conn.close()

    def create_table(self):
        #create a user table 
        # Create table statement
        self.conn = psycopg2.connect(
        database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
        )
        self.conn.autocommit = True
        cursor = self.conn.cursor()
        initial_check="DROP TABLE IF EXISTS userdetails;"
        sqlCreateUser = "create table userdetails (first_name varchar(256), last_name varchar(256), password varchar(256), email varchar(256) PRIMARY KEY);"
        # Create a table in PostgreSQL database
        cursor.execute(initial_check)
        cursor.execute(sqlCreateUser)
        self.conn.close()

    def add_security_data(self):
        None 

    def add_question_data(self):
        self.conn = psycopg2.connect(
        database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
        )
        self.conn.autocommit = True
        cursor = self.conn.cursor()
        for key, value in ques_dic.items(): 
            query= "Insert into questiondata (qid, question) values (%s, %s);"
            cursor.execute(query, [key, value])


    #insert values 

    def insert_values(self, data):
        self.conn = psycopg2.connect(
        database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
        )
        self.conn.autocommit = True
        cursor= self.conn.cursor()
        insert_query= "INSERT into userdetails (first_name, last_name, password, email) VALUES (%s, %s, %s, %s);"
        cursor.execute(insert_query, data) 
        self.conn.close()



    
        


