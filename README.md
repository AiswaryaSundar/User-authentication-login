# User-authentication-login

Two Schemas along with the two tables are created
  1. users for getting firstname,lastname,email,password
  2. UserDetails for entering user questions for security 

UserDetails : stores email along with 3 questions for that user and 3 answers given by him
              foreign key is email referencing from users details 

OTP : OTP verfification is implemented by using smpt library where random numbers are generated and are sent to 
      email provided by the user 
      
