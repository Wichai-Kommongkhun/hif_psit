from flask import Flask, render_template, request, redirect, url_for, session
from flask.helpers import flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt


"""
    ตรงนี้เป็นส่วนหลังบ้าน คนรับผิดชอบ มี BIG กับ โต้
    ทำการเชื่อมต่อ url เเต่ละเพจ เเละ ติดต่อ ฐานข้อมูล [ใช้ Myqsl]
"""

app = Flask(__name__)
app.secret_key = 'hif_psit'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user_account'



mysql = MySQL(app)
@app.route("/") #                   home page *
def home():
    return render_template('home.html')

@app.route("/bmi")#                   BMI page *
def bmi():
    return render_template("bmi.html")

@app.route("/hif_main")#                   hif_main page *
def main():
    return render_template("hif_main.html")

@app.route("/about")#                   about page *
def about():
    return render_template("about.html")

@app.route("/help")#                  help page *
def help():
    return render_template("help.html")

@app.route("/user_account/user_account_register", methods=['GET', 'POST'])#             register page *
def register():
    if request.method == 'POST' and 'user' \
    in request.form and 'password' in request.form and 'email' in request.form:
        user = request.form['user']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user = % s', (user, ))
        account = cursor.fetchone()
        if account: #ยังไม่ส่ง msg ไปหน้า reigiter
            msg = ''
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', user):
            msg = 'Username must contain only characters and numbers !'
        elif not user or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (user, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html')


@app.route("/user_account/user_account_login", methods=['GET','POST'])#               login page *
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['user'] = account['username']
            session['password'] = account['password']
            return redirect(url_for('home'))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template('login.html')
        

@app.route('/user_account/user_logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('user', None)
   session.pop('id', None)
   session.pop('user', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)
