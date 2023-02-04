import psycopg2


class Table():
    def __init__(self) -> None:
        conn= self.conn 


    def establish_connection(self):
        #establishing the connection
        self.conn = psycopg2.connect(
        database="postgres", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
        )
        self.conn.autocommit = True

        #Creating a cursor object using the cursor() method

    def create_table(self):
        #create a user table 
        # Create table statement
        cursor = self.conn.cursor()
        initial_check="DROP TABLE IF EXISTS UserDetails;"
        sqlCreateUser = "create table UserDetails (first varchar(256), last varchar(256), email varchar(256) PRIMARY KEY, number integer);"
        # Create a table in PostgreSQL database
        cursor.execute(initial_check)
        cursor.execute(sqlCreateUser)
        self.conn.close()

    #insert values 

    def insert_values(self, ques):
        cursor= self.conn.cursor()
        insert_query= "INSERT into employee(name, state) VALUES (%s, %s, %s, %d)"
        cursor.execute(insert_query) 
        self.conn.close()



Table.establish_connection()
Table.create_table()
    
        


