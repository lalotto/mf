import os
import smtplib
import csv
from flask import Flask, render_template, request, redirect

#Configure app
app = Flask(__name__)
 
#Registered students list
students = [] 

#Greeting user by the name through GET method /?n=John Doe
@app.route("/")
def index():
    n = request.args.get("n", "world")
    return render_template("index.html", name=n)  

#Print out registered people
@app.route("/registrants")
def registrants():
    with open("registered.csv", "r") as file:
        reader = csv.reader(file)
        students = list(reader)
    return render_template("registered.html", students=students)

#Getting user info from form by "POST"
@app.route("/register", methods=["POST"])
def register():
    from_mail = "antonov1985@gmail.com"
    from_mail_pass = ""
    name = request.form.get("name")
    email = request.form.get("email")
    dorm = request.form.get("dorm")
    if not name or not dorm or not email:
        return render_template("failure.html")
    students.append(f"{name} from {dorm}")

    #Send email to new member
    message = "You are registered!"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_mail, from_mail_pass)
    server.sendmail(from_mail, email, message)

    #Save input data to csv
    with open("registered.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((name, email, dorm))
    return redirect("/registrants")	