# User-authentication-login
*  Onboarding(name, email, password)
*  Security questions( 3 questions, ans from any 5 random)
*  Actual Login(3 factor login-username, password)
*  OTP Module(send email with OTP)
*  Verification of security questions(flash any three random question, the ans should match the prev one)
*  Integration of all modules
*  Database schema
*  Additional module(Encryption of the password.)

Two Schemas along with the two tables are created
  1. users for getting firstname,lastname,email,password
  2. UserDetails for entering user questions for security 

UserDetails : stores email along with 3 questions for that user and 3 answers given by him
              foreign key is email referencing from users details 

OTP : OTP verfification is implemented by using smpt library where random numbers are generated and are sent to 
      email provided by the user 
      
