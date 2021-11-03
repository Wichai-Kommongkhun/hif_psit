from flask import Flask, render_template, request, redirect, url_for, session
from flask.helpers import flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt
from datetime import datetime



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

@app.route("/home",methods=['POST', 'GET'] ) 
def home():
    name = "login"
    if request.method=='POST' and 'username' in request.form:
        username = (request.form["username"])

    return render_template('home.html')




@app.route("/bmi", methods=['POST','GET']) 
def bmi():
    day = ''
    bmi = ''
    msg = 'ไหนดูสิอ้วนรึป่าว?'
    name = ''
    if request.method=='POST' and 'weight' in request.form and 'height' in request.form:
        we = float(request.form['weight'])
        he = float(request.form['height'])
        bmi = we/((he/100)**2)
        bmi = '%.2f' %bmi
        if float(bmi) < 18.50 :
            msg = "☠ผอมเกินไปนะ"
        elif float(bmi) >= 18.50 and float(bmi) < 23.0:
            msg = " 💪สุขภาพดี!"
        elif float(bmi) >= 23 and float(bmi) < 25.0:
            msg = "🧸อวบ! ใกล้อ้วน"
        elif float(bmi) >= 25 and float(bmi) < 30.0:
            msg = "🐻อ้วนเเล้วนะ!"
        elif float(bmi) > 30.0:
            msg = "🐷อ้วนมากเลย ไปลดสะ!"
        today = datetime.today()
        today = today.strftime("%d/%m/%Y %H:%M")
        day = '%s' %today

    return render_template("bmi.html", bmi=bmi, msg = msg)


@app.route("/hif_main")
def main():
    return render_template("hif_main.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/help")
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
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (user, email, password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
        
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html')


@app.route("/user_account/user_account_login", methods=['GET','POST'])#      login page *
def login():
    session['user'] = 'Login'
    incor = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['user'] = account['user']
            session['password'] = account['password']
            return redirect(url_for('home'))
        else: # ใส่รหัสผิด
            incor = 'Incorrect username/password!'
    
    return render_template('login.html', incor=incor)
        

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
