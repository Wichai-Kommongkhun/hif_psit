from flask import Flask , template_rendered
from flask.templating import render_template


app = Flask(__name__)

@app.route("/") #                   home page *
def home():
    return render_template('home.html')

@app.route("/bmi")#                   BMI page *
def bmi():
    return render_template("bmi.html")

@app.route("/food")#                   food page *
def food():
    return render_template("food.html")

@app.route("/about")#                   about page *
def about():
    return render_template("about.html")

@app.route("/help")#                  help page *
def help():
    return render_template("help.html")

@app.route("/user_account_register")#             register page *
def register():
    return render_template("register.html")

@app.route("/user_account_login")#               login page *
def login():
    return render_template("login.html")



if __name__=="__main__":
    app.run(debug=True)
