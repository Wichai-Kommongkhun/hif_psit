from flask import Flask , template_rendered
from flask.templating import render_template


app = Flask(__name__)

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/bmi")
def bmi():
    return render_template("bmi.html")
@app.route("/bmi")
def bmi():
    return render_template("bmi.html")

if __name__=="__main__":
    app.run(debug=True)
