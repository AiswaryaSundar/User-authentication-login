import psycopg2
from Question import ques_dic


#establishing the connection
conn = psycopg2.connect(

   database="userauthentication", user='kirtipurohit', password='Aruba@123', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# initial_check="DROP TABLE IF EXISTS securitydata; DROP TABLE IF EXISTS questiondata;DROP TABLE IF EXISTS userdetails;"
# cursor.execute(initial_check)

# question_data= "create table questiondata (qid integer PRIMARY KEY, question varchar(256));"
# cursor.execute(question_data)
# for key, value in ques_dic.items(): 
#             query= "Insert into questiondata (qid, question) values (%s, %s);"
#             cursor.execute(query, [key, value])



sqlCreateUser = "create table userdetails (first_name varchar(256), last_name varchar(256), password varchar(256), email varchar(256) PRIMARY KEY);"
insert_query= "INSERT into userdetails (first_name, last_name, password, email) VALUES (%s, %s, %s, %s);"
data=[['kirti', 'purohit', 'gduge89w88y308', 'k@gmail.com'], ['abc', 'xyz', 'bdouwoebow', 'a@gmail.com'], 
      ['siddhi', 'pqrs', 'hiohpiew0eu40', 's@gmail.com']]

# cursor.execute(sqlCreateUser)
# for d in data:
#     cursor.execute(insert_query, d) 





# initial_check="DROP TABLE IF EXISTS securitydata;"
# user_security_data = "create table securitydata (email varchar(256), qid integer, CONSTRAINT email \
#       FOREIGN KEY(email) \
#       REFERENCES userdetails(email), CONSTRAINT qid FOREIGN KEY(qid) REFERENCES questiondata(qid), \
#       ans varchar(256), hint varchar(256), \
#       PRIMARY KEY(email, qid)  );"
# cursor.execute(initial_check) 
# cursor.execute(user_security_data)





securityDB_query= "insert into securitydata (email, qid, ans, hint) select userdetails.email, questiondata.qid, %s, %s \
    from userdetails, questiondata;"
data=['ice cream', 'cold']
cursor.execute(securityDB_query, data)




#Closing the connection
conn.close()