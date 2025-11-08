from flask import *
import sqlite3
from connect import con
app=Flask(__name__)
app.secret_key='abadf'



@app.route('/')
def home():
    return redirect('/adminhome')


@app.route("/reg")
def sreg():
    return render_template("register.html")
@app.route('/save',methods=['POST'])
def register():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        phonenumber=request.form['phonenumber']
        age=request.form['age']
        username=request.form['username']
        password=request.form['password']
        usertype=request.form['usertype']
        with sqlite3.connect('mydatabase.db')as con:

            cur=con.cursor()
            cur.execute('SELECT username FROM login WHERE username = ?', (username,))
            if cur.fetchone():
                # use flash instead of return 'Username already exists. Try another one.'
                flash('Username already exists. Try another one.')
                return redirect('/reg')   
            
            cur.execute('insert into login(username,password,usertype)values(?,?,?)',(username,password,usertype))
            loginid = cur.lastrowid

            if usertype=='student':
                cur.execute('insert into student (firstname,lastname ,age,email ,phone,loginid ) values(?,?,?,?,?,?)',(firstname,lastname ,age,email ,phonenumber,loginid ))
            
            elif usertype=='teacher':
                cur.execute('insert into teacher (firstname,lastname ,age,email ,phone,loginid ) values(?,?,?,?,?,?)',(firstname,lastname ,age,email ,phonenumber,loginid ))
            
            con.commit()
           
            return redirect('/login')




# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         uname = request.form['username']
#         pswd = request.form['password']
#        
#         con = sqlite3.connect('mydatabase.db')
#         con.row_factory = sqlite3.Row
#         cur = con.cursor()
#         cur.execute('SELECT * FROM login WHERE username=? AND password=?', (uname, pswd))
#         data = cur.fetchone()

#         if data:
#             session['logid'] = data['loginid']

#             if data['usertype'] == 'teacher' and data['status'] == '1':
#                 return redirect(url_for('teacherpage', loginid=data['loginid']))
#             elif data['usertype'] == 'student' and data['status'] == '1':
#                 return redirect(url_for('studentpage', loginid=data['loginid']))
#             elif uname == 'admin' and pswd == 'admin':
#                 return redirect(url_for("adminhome"))
#             else:
#                 return 'Sorry, not approved.'
#         else:
#             return 'Invalid username or password'

#     return render_template('login.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pswd = request.form['password']

        #  Always check admin first, so no DB hit needed.
        if uname == 'admin' and pswd == 'admin':
            return redirect(url_for("adminhome"))

        # Check normal users in DB
        with sqlite3.connect('mydatabase.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute( 'SELECT * FROM login WHERE username=? AND password=?',(uname, pswd))
            data = cur.fetchone()

            if data:
                session['logid'] = data['loginid']

                if data['status'] == 1 or str(data['status']) == '1':
                    # Only allow approved
                    if data['usertype'] == 'teacher':
                        return redirect(url_for('teacherpage', loginid=data['loginid']))
                    elif data['usertype'] == 'student':
                        return redirect(url_for('studentpage', loginid=data['loginid']))
                else:
                    # return 'Sorry, your account is not approved yet.'
                    flash('Sorry, your account is not approved yet.')


        # If no match or wrong password
        # return 'Invalid username or password'
        flash( 'Invalid username or password')


    #  If GET method: show form
    return render_template('login.html')

@app.route("/adminhome", methods=['GET', 'POST'])
def adminhome():
    con = sqlite3.connect('mydatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Handle approval form submission
    if request.method == 'POST':
        user_id = request.form['id']
        user_type = request.form['type']

        if user_type == 'student':
            cur.execute("UPDATE login SET status=1 WHERE loginid=(SELECT loginid FROM student WHERE sid=?)", (user_id,))
            cur.execute("UPDATE student SET status=1 WHERE sid=?", (user_id,))
        elif user_type == 'teacher':
            cur.execute("UPDATE login SET status=1 WHERE loginid=(SELECT loginid FROM teacher WHERE tid=?)", (user_id,))
            cur.execute("UPDATE teacher SET status=1 WHERE tid=?", (user_id,))
        
        con.commit()
        flash("User approved successfully!")
        return redirect(url_for('adminhome'))

    # Fetch all students and teachers
    cur.execute("SELECT * FROM student")
    students = cur.fetchall()
    cur.execute("SELECT * FROM teacher")
    teachers = cur.fetchall()

    con.close()
    return render_template("adminhome.html", students=students, teachers=teachers)



@app.route("/deletedetail/<int:loginid>")
def deletedetail(loginid):
    con = sqlite3.connect('mydatabase.db')
    cursor = con.cursor()

    # Delete from student where loginid matches
    cursor.execute("DELETE FROM student WHERE loginid = ?", (loginid,))

    # Delete from teacher where loginid matches
    cursor.execute("DELETE FROM teacher WHERE loginid = ?", (loginid,))

    # Delete from login table
    cursor.execute("DELETE FROM login WHERE loginid = ?", (loginid,))

    con.commit()
    con.close()

    return redirect("/adminhome")

@app.route("/approve/<int:loginid>")
def approve(loginid):
    con = sqlite3.connect('mydatabase.db')
    cursor = con.cursor()

    # Update status in all three tables just in case
    cursor.execute("UPDATE login SET status=1 WHERE loginid=?", (loginid,))
    cursor.execute("UPDATE teacher SET status=1 WHERE loginid=?", (loginid,))
    cursor.execute("UPDATE student SET status=1 WHERE loginid=?", (loginid,))

    con.commit()
    con.close()

    return redirect("/adminhome")



@app.route("/teacher/<int:loginid>")
def teacherpage(loginid):
    if 'logid' not in session or session['logid'] != loginid:
        return redirect(url_for('login'))

    con = sqlite3.connect('mydatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Get this teacher's profile
    cur.execute("SELECT * FROM teacher WHERE loginid = ?", (loginid,))
    teacher = cur.fetchone()

    # Get approved students
    cur.execute("SELECT * FROM student WHERE status = 1")
    students = cur.fetchall()

    con.close()

    return render_template("teacherpage.html", teacher=teacher, students=students)



@app.route("/editteacher/<int:tid>")
def editteacher(tid):
    if 'logid' not in session:
        return redirect(url_for('login'))
    con=sqlite3.connect('mydatabase.db')
    con.row_factory=sqlite3.Row
    cursor3=con.cursor()
    cursor3.execute("select * from teacher where tid=?",(tid,))
    data=cursor3.fetchone()
    return render_template("editteacher.html",data=data)

@app.route("/updateteacher/<int:tid>",methods=["POST"])
def updateteacher(tid):
    if 'logid' not in session:
        return redirect(url_for('login'))
    con=sqlite3.connect('mydatabase.db')
    con.row_factory=sqlite3.Row
    cursor5=con.cursor()
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    email=request.form['email']
    age=request.form['age']
    phone=request.form['phonenum']
    cursor5.execute("update teacher set firstname=?,lastname=?,email=?,age=?,phone=? where tid=?",(firstname,lastname,email,age,phone,tid))
    cursor5.execute("SELECT loginid FROM teacher WHERE tid = ?", (tid,))
    teacher = cursor5.fetchone()
    loginid = teacher['loginid']
    con.commit()
    con.close()
    session['logid'] = loginid
    return redirect(url_for('teacherpage', loginid=loginid))


@app.route('/logout')
def logout():
    # Remove the session key(s)
    session.pop('logid', None)
    # Redirect to login page (or home)
    return redirect(url_for('login'))

@app.route("/student/<int:loginid>")
def studentpage(loginid):
    if 'logid' not in session or session['logid'] != loginid:
        return redirect(url_for('login'))

    con = sqlite3.connect('mydatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM student WHERE loginid = ?", (loginid,))
    student = cur.fetchone()

    cur.execute("SELECT * FROM teacher WHERE status = 1")
    teachers = cur.fetchall()
    con.close()

    return render_template("studentpage.html", student=student, teachers=teachers)

@app.route("/editstudent/<int:sid>")
def editstudent(sid):
    if 'logid' not in session:
        return redirect(url_for('login'))

    con = sqlite3.connect('mydatabase.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM student WHERE sid = ?", (sid,))
    student = cur.fetchone()
    con.close()

    return render_template("editstudent.html", data=student)



@app.route("/updatestudent/<int:sid>",methods=["POST"])
def updatestudent(sid):
    if 'logid' not in session:
        return redirect(url_for('login'))
    
    con=sqlite3.connect('mydatabase.db')
    con.row_factory=sqlite3.Row
    cursor5=con.cursor()

    firstname=request.form['firstname']
    lastname=request.form['lastname']
    email=request.form['email']
    age=request.form['age']
    phone=request.form['phonenum']

    cursor5.execute("update student set firstname=?,lastname=?,email=?,age=?,phone=? where sid=?",(firstname,lastname,email,age,phone,sid))
    
    cursor5.execute("SELECT loginid FROM student WHERE sid = ?", (sid,))
    student = cursor5.fetchone()
    loginid = student['loginid']

    con.commit()
    con.close()

    return redirect(url_for('studentpage', loginid=loginid))



if __name__=="__main__":
    app.run(debug=True)