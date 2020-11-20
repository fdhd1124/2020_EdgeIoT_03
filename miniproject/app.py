from flask import Flask, render_template 
from flask import request, url_for, redirect
import pymysql

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/new_member', methods=['POST','GET'])
def new_member():
    if request.method == 'POST':
        nm = request.form['nm']
        phone = request.form['phone']
        email = request.form['email']

        conn = pymysql.connect(host="192.168.100.41", user="raspberryPi", password="Ab1!", db="memberdb", charset='utf8',port=9876)
        curr = conn.cursor()
        sql = "INSERT INTO info values('"+str(nm) +"','"+str(phone)+"','"+str(email)+"')"
        print(sql)
        curr.execute(sql)
        conn.commit()
    
        curr.close()
        conn.close()
        conn = None
        curr = None
        return render_template('index.html')

@app.route('/join')
def join():
    return render_template('new_member.html')

@app.route('/info')
def info():
    return redirect(url_for('list'))
    return render_template('member_information.html')

@app.route('/check_in')
def check_in():
    return redirect(url_for('list2'))
    return render_template('check_in_management.html')
    
@app.route('/list')
def list():
    con = pymysql.connect(host="192.168.100.41", user="raspberryPi", password="Ab1!", db="memberdb", charset='utf8', port=9876)
    cur = con.cursor()
    cur.execute("select * from info")
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
        print(type(row))

    cur.close()
    con.close()
    return render_template("member_information.html",rows = rows)


@app.route('/list2')
def list2():
    con = pymysql.connect(host="192.168.100.41", user="raspberryPi", password="Ab1!", db="memberdb", charset='utf8', port=9876)
    cur = con.cursor()
    cur.execute("select * from login_log3")
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
        print(type(row))

    cur.close()
    con.close()
    return render_template("check_in_management.html",rows = rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

