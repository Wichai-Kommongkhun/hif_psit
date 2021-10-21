from flask import Flask , template_rendered
from flask.templating import render_template


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/bmi")
def bmi():
    return render_template("bmi.html")

@app.route("/user_account_register")
def register():
    return render_template("register.html")

@app.route("/user_account_login")
def login():
    return render_template("login.html")



if __name__=="__main__":
    app.run(debug=True)
