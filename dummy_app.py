from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date
import re
import os
import sys
    
app = Flask(__name__)
   
app.secret_key = 'abcd21234455'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vedavyas'
app.config['MYSQL_DB'] = 'dummy'
  
mysql = MySQL(app)
  
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template("main.html")

# @app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']        
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE status="Admin" AND email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['UsernameId']
            session['name'] = user['FirstName']
            session['email'] = user['Email']
            mesage = 'Logged in successfully !'            
            return redirect(url_for('dashboard'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
    
# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     mesage = ''
#     if request.method == 'POST':
#         email = request.form['email']        
#         password = request.form['password']
#         UsernameId = request.form['UsernameId']
#         FirstName = request.form['FirstName']
#         LastName = request.form['LastName']
#         PhoneNumber = request.form['PhoneNumber']
#         Gender = request.form['Gender']  
#         Status = request.form['Status']  
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(f"INSERT INTO user( email, password, UsernameId, FirstName, LastName, PhoneNumber, Gender, Status) \
#                        values('{email}','{password}','{UsernameId}','{FirstName}','{LastName}','{PhoneNumber}','{Gender}','{Status}')")
#         mysql.connection.commit()
#         cursor.close()

#         return redirect(url_for('login'))
    
#     return render_template('register.html', mesage = mesage)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'email' in \
    request.form and 'password' in request.form and \
    'UsernameId' in request.form and 'FirstName' in \
    request.form and 'LastName' in request.form and \
    'PhoneNumber' in request.form and 'Gender' \
    in request.form and 'Status' in request.form:
        UsernameId = request.form['UsernameId']
        password = request.form['password']
        email = request.form['email']        
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        PhoneNumber = request.form['PhoneNumber']
        Gender = request.form['Gender']  
        Status = request.form['Status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', email):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user (UsernameId, password, email, FirstName, LastName, PhoneNumber, Gender, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
               (UsernameId, password, email, FirstName, LastName, PhoneNumber, Gender, Status))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    # if 'loggedin' in session:
    if request.method == 'POST' and 'email' in \
    request.form and 'password' in request.form and \
    'UsernameId' in request.form and 'FirstName' in \
    request.form and 'LastName' in request.form and \
    'PhoneNumber' in request.form and 'Gender' \
    in request.form and 'Status' in request.form:
        email = request.form['email']        
        password = request.form['password']
        UsernameId = request.form['UsernameId']
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        PhoneNumber = request.form['PhoneNumber']
        Gender = request.form['Gender']  
        Status = request.form['Status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        items = cursor.fetchall()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', email):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('UPDATE user SET email =% s,\
            password =% s, UsernameId =% s, FirstName =% s, \
            LastName =% s, PhoneNumber =% s, Gender =% s, \
            Status =% s WHERE email =% s', (
                email, password, UsernameId, FirstName, 
                LastName, PhoneNumber, Gender, Status, 
                (session['email'], ), ))
            mysql.connection.commit()
            msg = 'You have successfully updated !'
        # elif request.method == 'POST':
        #     msg = 'Please fill out the form !'
        return render_template("update.html", items=items,msg=msg)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/profile', methods =['GET'])
def profile():
    if 'loggedin' in session: 
        UsernameId = request.args.get('UsernameId') 
        print(UsernameId)      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT UsernameId,FirstName,LastName, concat(FirstName,LastName) as Name, Email, PhoneNumber, Gender from Students where UsernameId=%s',(UsernameId,))
        user = cursor.fetchall() 
        
        # cursor.execute('SELECT * FROM classes')
        # classes = cursor.fetchall() 
        
        # cursor.execute('SELECT * FROM section')
        # sections = cursor.fetchall()
        # return render_template("student.html", students = students, classes = classes, sections = sections)
        return render_template("profile.html", user=user)
    return redirect(url_for('login'))
    
@app.route("/dashboard", methods =['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:        
        return render_template("dashboard.html")
    return redirect(url_for('login'))    


########################### Teacher section ##################################
@app.route("/teacher", methods =['GET', 'POST'])
def teacher():
    if 'loggedin' in session:   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT *,concat(Firstname,LastName) as Name from faculty')
        teachers = cursor.fetchall() 
           
        cursor.execute('SELECT * FROM courses')
        subjects = cursor.fetchall()  
        return render_template("teacher.html", teachers = teachers, subjects = subjects)
    return redirect(url_for('login')) 
	
    # Teacher_Id, FirstName, LastName, Expertise, YearsOfExperience, Recognitions, Email, Department, status, Course_Id, OfficeHours
	# '104_Emily', 'Emily', 'Clark', 'emily.clark@example.com', 'password456', '9876543210', 'female', 'Teacher'

@app.route("/edit_teacher", methods =['GET'])
def edit_teacher():
    if 'loggedin' in session:
        Teacher_Id = request.args.get('Teacher_Id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from faculty WHERE Teacher_Id = %s', (Teacher_Id,))
        teachers = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM courses')
        subjects = cursor.fetchall()  
        
        return render_template("edit_teacher.html", teachers = teachers, subjects = subjects)
    return redirect(url_for('login'))  
    
	
@app.route("/save_teacher", methods =['GET', 'POST'])
def save_teacher():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
		# if request.method == 'POST' and 'techer_name' in request.form and 'specialization' in request.form:	
		
        if request.method == 'POST' and 'Teacher_Id' in request.form and 'FirstName' in request.form \
		and 'LastName' in request.form and 'Expertise' in request.form and 'YearsOfExperience' in request.form \
		and 'Recognitions' in request.form and 'Email' in request.form and 'Department' in request.form \
		and 'OfficeHours' in request.form and 'Course_Id' in request.form:
            Teacher_Id = request.form['Teacher_Id'] 
            FirstName = request.form['FirstName'] 
            LastName = request.form['LastName'] 
            Expertise = request.form['Expertise'] 
            YearsOfExperience = request.form['YearsOfExperience'] 
            Recognitions = request.form['Recognitions'] 
            Email = request.form['Email'] 
            Department = request.form['Department'] 
            OfficeHours = request.form['OfficeHours'] 
            Course_Id = request.form['Course_Id'] 
            action = request.form['action']             
            
            if action == 'updateTeacher':
                Teacher_Id = request.form['Teacher_Id']  
                FirstName = request.form['FirstName'] 
                LastName = request.form['LastName'] 
                Expertise = request.form['Expertise'] 
                YearsOfExperience = request.form['YearsOfExperience'] 
                Recognitions = request.form['Recognitions'] 
                Email = request.form['Email'] 
                Department = request.form['Department'] 
                OfficeHours = request.form['OfficeHours'] 
                Course_Id = request.form['Course_Id'] 
                cursor.execute('UPDATE faculty \
                   SET FirstName = %s, LastName = %s, Expertise = %s, YearsOfExperience = %s, \
                   Recognitions = %s, Email = %s, Department = %s, Course_Id = %s, OfficeHours = %s \
				    WHERE Teacher_Id =%s', (FirstName, LastName, Expertise, YearsOfExperience, Recognitions, Email, Department, Course_Id, OfficeHours, (Teacher_Id, ), ))
                # cursor.execute('UPDATE teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))

                mysql.connection.commit()
				# cursor.execute('UPDATE faculty \
                #    SET FirstName = %s, LastName = %s, Expertise = %s, YearsOfExperience = %s, \
                #    Recognitions = %s, Email = %s, Department = %s, status, Course_Id = %s, OfficeHours = %s \
				#     WHERE Teacher_Id =% s', (FirstName, LastName, Expertise, YearsOfExperience, Recognitions, Email, Department, Course_Id, OfficeHours, (Teacher_Id, ), ))
                # # cursor.execute('UPDATE sms_teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))
                # mysql.connection.commit()           
            else: 
            #     # cursor.execute('INSERT INTO teacher (`teacher`, `subject_id`) VALUES (%s, %s)', (techer_name, specialization))
                cursor.execute('INSERT INTO faculty (Teacher_Id, FirstName, LastName, Expertise, YearsOfExperience, Recognitions, \
				Email, Department, Course_Id, OfficeHours) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)', (Teacher_Id, FirstName, LastName, Expertise, \
				YearsOfExperience, Recognitions, Email, Department, Course_Id, OfficeHours))

                mysql.connection.commit()      
            return redirect(url_for('teacher'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('teacher'))        
    return redirect(url_for('login')) 
 

 
@app.route("/delete_teacher", methods =['GET'])
def delete_teacher():
    if 'loggedin' in session:
        Teacher_Id = request.args.get('Teacher_Id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM faculty WHERE Teacher_Id = % s', (Teacher_Id, ))
        mysql.connection.commit()   
        return redirect(url_for('teacher'))
    return redirect(url_for('login'))
    

########################### Teacher section ##################################

# @app.route("/faculty", methods =['GET', 'POST'])
# def teacher():
#     if 'loggedin' in session:   
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # cursor.execute('SELECT t.teacher_id, t.teacher, s.subject FROM teacher t LEFT JOIN subjects s ON s.subject_id = t.subject_id')
#         cursor.execute('select Teacher_Id, concat(FirstName,LastName) as Name, Department from faculty')
#         teachers = cursor.fetchall() 
           
#         cursor.execute('SELECT * FROM courses')
#         subjects = cursor.fetchall()  
#         return render_template("teacher.html", teachers = teachers, subjects = subjects)
#     return redirect(url_for('login')) 
    
# @app.route("/edit_teacher", methods =['GET'])
# def edit_teacher():
#     if 'loggedin' in session:
#         Teacher_Id = request.args.get('Teacher_Id') 
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # cursor.execute('SELECT t.teacher_id, t.teacher, s.subject FROM teacher t LEFT JOIN subjects s ON s.subject_id = t.subject_id WHERE t.Teacher_Id = %s', (teacher_id,))
#         cursor.execute('select * from faculty where Teacher_Id = %s', (Teacher_Id,))

#         teachers = cursor.fetchall() 
        
#         cursor.execute('SELECT * FROM courses')
#         subjects = cursor.fetchall()  
        
#         return render_template("edit_teacher.html", teachers = teachers, subjects = subjects)
#     return redirect(url_for('login'))  
    
# @app.route("/save_teacher", methods =['GET', 'POST'])
# def save_teacher():
#     if 'loggedin' in session:    
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
#         if request.method == 'POST' and 'Teacher_Id' in request.form \
#             and 'FirstName' in request.form and 'LastName' in request.form \
#             and 'Email' in request.form and 'Expertise' in request.form \
#             and 'YearsOfExperience' in request.form and 'Recognitions' in request.form \
#             and 'Department' in request.form \
#         and 'OfficeHours' in request.form and 'Course_Id' in request.form:
#             Teacher_Id = request.form['Teacher_Id'] 
#             FirstName = request.form['FirstName'] 
#             LastName = request.form['LastName'] 
#             Email = request.form['Email'] 
#             Expertise = request.form['Expertise'] 
#             YearsOfExperience = request.form['YearsOfExperience'] 
#             Recognitions = request.form['Recognitions'] 
#             Department = request.form['Department'] 
#             OfficeHours = request.form['OfficeHours']   
#             Course_Id = request.form['Course_Id']          
#             action = request.form['action']             
            
#             if action == 'updateTeacher':
#                 Teacher_Id = request.form['Teacher_Id'] 
#                 FirstName = request.form['FirstName'] 
#                 LastName = request.form['LastName'] 
#                 Email = request.form['Email'] 
#                 Expertise = request.form['Expertise'] 
#                 YearsOfExperience = request.form['YearsOfExperience'] 
#                 Recognitions = request.form['Recognitions'] 
#                 Department = request.form['Department'] 
#                 OfficeHours = request.form['OfficeHours']   
#                 Course_Id = request.form[Course_Id]     
#                 cursor.execute('UPDATE faculty \
#                                SET FirstName = %s, LastName = %s,FirstName = %s, Expertise = %s, \
#                                YearsOfExperience = %s, Recognitions = %s,Email = %s, Department = %s, \
#                                Course_Id = %s, OfficeHours = %s WHERE Teacher_Id =% s', 
#                                 (FirstName,LastName,Expertise,YearsOfExperience,Recognitions,Email,Department,
#                                  Course_Id, OfficeHours, (Teacher_Id, ), ))
#                 # cursor.execute('UPDATE teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))

#                 mysql.connection.commit()        
#             else: 
#                 # cursor.execute('INSERT INTO teacher (`teacher`, `subject_id`) VALUES (%s, %s)', (techer_name, specialization))
#                 cursor.execute('INSERT INTO teacher \
#                                (Teacher_Id, FirstName, LastName,  Expertise, YearsOfExperience, Recognitions, Email, Department, Course_Id,OfficeHours) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)', 
#                                (Teacher_Id,FirstName,LastName,Expertise,YearsOfExperience,Recognitions,Email,Department,
#                                  Course_Id, OfficeHours))

#                 mysql.connection.commit()        
#             return redirect(url_for('faculty'))        
#         elif request.method == 'POST':
#             msg = 'Please fill out the form field !'        
#         return redirect(url_for('faculty'))        
#     return redirect(url_for('login')) 
    
# @app.route("/delete_teacher", methods =['GET'])
# def delete_teacher():
#     if 'loggedin' in session:
#         Teacher_Id = request.args.get('Teacher_Id') 
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('DELETE FROM faculty WHERE Teacher_Id = % s', (Teacher_Id, ))
#         mysql.connection.commit()   
#         return redirect(url_for('faculty'))
#     return redirect(url_for('login'))
    
########################### COURSES ##################################
    
@app.route("/courses", methods =['GET', 'POST'])
def subject():
    if 'loggedin' in session:       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM courses')
        subjects = cursor.fetchall() 

        cursor.execute('SELECT * FROM faculty')
        teachers = cursor.fetchall()

        return render_template("subject.html", subjects = subjects, teachers = teachers)
    return redirect(url_for('login'))

@app.route("/edit_subject", methods =['GET'])
def edit_subject():
    if 'loggedin' in session:
        course_id = request.args.get('course_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
        subjects = cursor.fetchall() 

        cursor.execute('SELECT * FROM faculty')
        teachers = cursor.fetchall()

        return render_template("edit_subject.html", subjects = subjects, teachers = teachers )
    return redirect(url_for('login'))  

@app.route("/save_subject", methods =['GET', 'POST'])
def save_subject():
    if 'loggedin' in session:  
        course_id = request.args.get('course_id')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
       
        if request.method == 'POST' and 'course_id' in request.form and 'faculty_id' in request.form and \
        'course_name' in request.form and 'topics_covered' in request.form and 'rating' in request.form :
            course_id = request.form['course_id'] 
            faculty_id = request.form['faculty_id'] 
            course_name = request.form['course_name'] 
            topics_covered = request.form['topics_covered']
            rating = request.form['rating']              
            action = request.form['action']             
            
            if action == 'updateSubject':
                course_id = request.form['course_id'] 
                faculty_id = request.form['faculty_id'] 
                course_name = request.form['course_name'] 
                topics_covered = request.form['topics_covered']
                rating = request.form['rating'] 
                # subjectid = request.form['subjectid'] 
                cursor.execute('UPDATE courses SET faculty_id = %s, course_name = %s, topics_covered = %s, rating = %s WHERE course_id =% s', (faculty_id, course_name, topics_covered, rating, (course_id,  ), ))
                mysql.connection.commit()        
            else: 
                cursor.execute('INSERT INTO courses (course_id, faculty_id, course_name, topics_covered, rating) VALUES (%s,%s, %s, %s, %s)', (course_id, faculty_id, course_name, topics_covered, rating ))
                mysql.connection.commit()        
            return redirect(url_for('subject'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('subject'))        
    return redirect(url_for('login'))   
    
@app.route("/delete_subject", methods =['GET'])
def delete_subject():
    if 'loggedin' in session:
        course_id = request.args.get('course_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM courses WHERE course_id = % s', (course_id, ))
        mysql.connection.commit()   
        return redirect(url_for('subject'))
    return redirect(url_for('login'))

################################ Classes  #######################################

@app.route("/classes", methods =['GET', 'POST'])
def classes():
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall() 
           
        # cursor.execute('SELECT * FROM section')
        # sections = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM faculty')
        teachers = cursor.fetchall()
        
        # return render_template("class.html", classes = classes, sections = sections, teachers = teachers)
        return render_template("class.html", classes = classes, teachers = teachers)
    return redirect(url_for('login'))

@app.route("/edit_class", methods =['GET'])
def edit_class():
    if 'loggedin' in session:
        class_id = request.args.get('class_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from classes WHERE class_id = %s', (class_id,))
        classes = cursor.fetchall() 
        
        # cursor.execute('SELECT * FROM section')
        # sections = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM faculty')
        teachers = cursor.fetchall()
        
        return render_template("edit_class.html", classes = classes, teachers = teachers)
    return redirect(url_for('login'))  

@app.route("/save_class", methods =['GET', 'POST'])
def save_class():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
             
        if request.method == 'POST' and 'class_id' in request.form \
        and 'class_name' in request.form  and 'class_teacher_id' in request.form and 'Department' in request.form:
            class_id = request.form['class_id'] 
            class_name = request.form['class_name']
            class_teacher_id = request.form['class_teacher_id']  
            Department = request.form['Department']          
            action = request.form['action']             
            
            if action == 'updateClass':
                class_id = request.form['class_id'] 
                cursor.execute('UPDATE classes SET class_name = %s, class_teacher_id = %s, Department = %s WHERE class_id  =%s', (class_name, class_teacher_id, Department, (class_id, ), ))
                mysql.connection.commit()        
            else: 
                cursor.execute('INSERT INTO classes (class_id, class_name, class_teacher_id, Department ) VALUES (%s, %s, %s, %s)', (class_id, class_name, class_teacher_id, Department))
                mysql.connection.commit()        
            return redirect(url_for('classes'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('classes'))        
    return redirect(url_for('login'))
    

@app.route("/delete_class", methods =['GET'])
def delete_class():
    if 'loggedin' in session:
        class_id = request.args.get('class_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM classes WHERE class_id = % s', (class_id, ))
        mysql.connection.commit()   
        return redirect(url_for('classes'))
    return redirect(url_for('login'))     

########################### SECTIONS ##################################

@app.route("/sections", methods =['GET', 'POST'])
def sections():
    if 'loggedin' in session:      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM section')
        sections = cursor.fetchall()          
        return render_template("sections.html", sections = sections)
    return redirect(url_for('login')) 
    
@app.route("/edit_sections", methods =['GET'])
def edit_sections():
    if 'loggedin' in session:
        section_id = request.args.get('section_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM section WHERE section_id = %s', (section_id,))
        sections = cursor.fetchall() 
        return render_template("edit_section.html", sections = sections)
    return redirect(url_for('login'))    
    
@app.route("/save_sections", methods =['GET', 'POST'])
def save_sections():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        if request.method == 'POST' and 'section_name' in request.form:
            section_name = request.form['section_name']                         
            action = request.form['action']             
            
            if action == 'updateSection':
                section_id = request.form['sectionid'] 
                cursor.execute('UPDATE section SET section = %s WHERE section_id  =%s', (section_name, (section_id, ), ))
                mysql.connection.commit()        
            else: 
                cursor.execute('INSERT INTO section (`section`) VALUES (%s)', (section_name, ))
                mysql.connection.commit()        
            return redirect(url_for('sections'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('sections'))        
    return redirect(url_for('login')) 
    
@app.route("/delete_sections", methods =['GET'])
def delete_sections():
    if 'loggedin' in session:
        section_id = request.args.get('section_id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM section WHERE section_id = % s', (section_id, ))
        mysql.connection.commit()   
        return redirect(url_for('sections'))
    return redirect(url_for('login'))  

########################### STUDENTS ##################################
    
@app.route("/student", methods =['GET', 'POST'])
def student():
    if 'loggedin' in session:       
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT *,concat(FirstName,LastName) as Name from Students')
        students = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall() 
        
        # cursor.execute('SELECT * FROM section')
        # sections = cursor.fetchall()
        # return render_template("student.html", students = students, classes = classes, sections = sections)
        return render_template("student.html", students = students, classes = classes)
    return redirect(url_for('login')) 
    
@app.route("/edit_student", methods =['GET'])
def edit_student():
    if 'loggedin' in session:
        StudentId = request.args.get('StudentId') 
        print(StudentId)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT *,concat(FirstName,LastName) as Name from Students WHERE StudentId = %s', (StudentId,))
        students = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM faculty')
        teachers = cursor.fetchall()
        # return render_template("edit_student.html", students = students, classes = classes, sections = sections)
        return render_template("edit_student.html", students = students, classes = classes, teachers=teachers)
    return redirect(url_for('login'))  

@app.route("/save_student", methods =['GET', 'POST'])
def save_student():
    print("HII im in ")
    if 'loggedin' in session:  
        print("session loggeedd !!!")  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        print(request.form) 
		# if request.method == 'POST' and 'techer_name' in request.form and 'specialization' in request.form:	
		

        if request.method == 'POST' and 'StudentId' in request.form and 'FirstName' in request.form \
		and 'LastName' in request.form and 'Phone' in request.form  \
		and 'CoursesTaken' in request.form and 'Email' in request.form and 'Department' in request.form \
        and 'Address' in request.form and 'ClassId' in request.form and 'Stream' in request.form \
        and 'AdmissionDate' in request.form and 'AcademicYear' in request.form and 'classteacher' in request.form \
		and 'AdmissionNo' in request.form :
            print(" first :")
            StudentId = request.form['StudentId'] 
            FirstName = request.form['FirstName'] 
            LastName = request.form['LastName'] 
            Phone = request.form['Phone'] 
            # Gender = request.form['Gender'] 
            CoursesTaken = request.form['CoursesTaken'] 
            Email = request.form['Email'] 
            Department = request.form['Department'] 
            AdmissionNo = request.form['AdmissionNo'] 
            # Course_Id = request.form['Course_Id'] 
            Address = request.form['Address']
            ClassId = request.form['ClassId']
            Stream = request.form['Stream']
            AdmissionDate = request.form['AdmissionDate']
            AcademicYear = request.form['AcademicYear']
            classteacher = request.form['classteacher']
            # status = request.form['status']
            action = request.form['action']             
            
            if action == 'updateStudent':
                print("Secpond : ")
                StudentId = request.form['StudentId'] 
                FirstName = request.form['FirstName'] 
                LastName = request.form['LastName'] 
                Phone = request.form['Phone'] 
                # Gender = request.form['Gender'] 
                CoursesTaken = request.form['CoursesTaken'] 
                Email = request.form['Email'] 
                Department = request.form['Department'] 
                AdmissionNo = request.form['AdmissionNo'] 
                # Course_Id = request.form['Course_Id'] 
                Address = request.form['Address']
                ClassId = request.form['ClassId']
                Stream = request.form['Stream']
                AdmissionDate = request.form['AdmissionDate']
                AcademicYear = request.form['AcademicYear']
                classteacher = request.form['classteacher'] 
                cursor.execute('UPDATE students \
                   SET FirstName = %s, LastName = %s, Email = %s, Phone = %s, \
                   CoursesTaken = %s, AdmissionNo = %s, Address = %s, ClassId = %s, Stream = %s, \
                Department = %s, AdmissionDate = %s, AcademicYear = %s, classteacher = %s \
				    WHERE StudentId =%s', (FirstName, LastName, Email, Phone, CoursesTaken, AdmissionNo, Address, ClassId,
Stream, Department, AdmissionDate, AcademicYear, classteacher,  (StudentId, ), ))
                print(FirstName, LastName, Email, Phone, CoursesTaken, AdmissionNo, Address, ClassId,
Stream, Department, AdmissionDate, AcademicYear, classteacher)
                
                # cursor.execute('UPDATE teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))

                mysql.connection.commit()
				# cursor.execute('UPDATE faculty \
                #    SET FirstName = %s, LastName = %s, Phone = %s, Gender = %s, \
                #    CoursesTaken = %s, Email = %s, Department = %s, status, Course_Id = %s, AdmissionNo = %s \
				#     WHERE Teacher_Id =% s', (FirstName, LastName, Phone, Gender, CoursesTaken, Email, Department, Course_Id, AdmissionNo, (Teacher_Id, ), ))
                # # cursor.execute('UPDATE sms_teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))
                # mysql.connection.commit()           
            else:
                print("finally")
                print(request.form) 
            #     # cursor.execute('INSERT INTO teacher (`teacher`, `subject_id`) VALUES (%s, %s)', (techer_name, specialization))
                cursor.execute('INSERT INTO students (StudentId, FirstName, LastName, Email, Phone, CoursesTaken, AdmissionNo, Address, ClassId,\
Stream, Department, AdmissionDate, AcademicYear, classteacher) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)', (StudentId, FirstName, LastName, Email, Phone, CoursesTaken, AdmissionNo, Address, ClassId,
Stream, Department, AdmissionDate, AcademicYear, classteacher))

                mysql.connection.commit()      
            return redirect(url_for('student'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('student'))        
    return redirect(url_for('login')) 
 


# def save_student():
#     if 'loggedin' in session:    
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
#         if request.method == 'POST' and 'section_name' in request.form:
#             section_name = request.form['section_name']                         
#             action = request.form['action']             
            
#             if action == 'updateStudent':
#                 section_id = request.form['sectionid'] 
#                 cursor.execute('UPDATE section SET section = %s WHERE section_id  =%s', (section_name, (section_id, ), ))
#                 mysql.connection.commit()        
#             else: 
#                 cursor.execute('INSERT INTO section (`section`) VALUES (%s)', (section_name, ))
#                 mysql.connection.commit()        
#             return redirect(url_for('sections'))        
#         elif request.method == 'POST':
#             msg = 'Please fill out the form field !'        
#         return redirect(url_for('sections'))        
#     return redirect(url_for('login'))     
    
@app.route("/delete_student", methods =['GET'])
def delete_student():
    if 'loggedin' in session:
        StudentId = request.args.get('StudentId') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM students WHERE StudentId = % s', (StudentId, ))
        mysql.connection.commit()   
        return redirect(url_for('student'))
    return redirect(url_for('login'))  

########################### STUDENT ATTENDANCE ##################################

@app.route("/studentAttendance", methods =['GET', 'POST'])
def studentAttendance():
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM updateAttendance')
        student_attendance = cursor.fetchall()

        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall() 

        cursor.execute('SELECT *,concat(FirstName,LastName) as Name FROM students')
        students = cursor.fetchall()

        return render_template("attendance.html", classes = classes, students=students, student_attendance = student_attendance)
    return redirect(url_for('login')) 
    
    
@app.route("/getClassAttendance", methods =['GET', 'POST'])
def getClassAttendance():
    if 'loggedin' in session:
        print('Started!!')  
        if request.method == 'POST' or 'class_id' in request.form:
        
            class_id = request.form['class_id']
            # StudentId = request.form['StudentId']

            print('class_id')
            print(class_id)
            # sectionid = request.form['sectionid']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
            
            cursor.execute('SELECT * FROM classes')
            classes = cursor.fetchall() 
            
            # cursor.execute('SELECT * FROM section')
            # sections = cursor.fetchall() 
            cursor.execute('SELECT * FROM updateAttendance where class_id = %s', (class_id, ))
            student_attendance = cursor.fetchall()

            currentDate = date.today().strftime('%Y/%m/%d')
                     
            # cursor.execute('SELECT s.id, s.name, s.photo, s.gender, s.dob, s.mobile, s.email, s.current_address, s.father_name, s.mother_name,s.admission_no, s.roll_no, s.admission_date, s.academic_year, a.attendance_status, a.attendance_date FROM students as s LEFT JOIN attendance as a ON s.id = a.student_id WHERE s.class = '+classid+' AND s.section = '+sectionid)              
            # cursor.execute('SELECT *,concat(FirstName,LastName) as Name from Students')
            # students = cursor.fetchall()   
                      
            return render_template("attendance.html", classes = classes,  class_id = class_id, student_attendance = student_attendance)        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('studentAttendance'))        
    return redirect(url_for('login'))

# @app.route("/update_attendance", methods =['GET'])
# def update_attendance():
#     if 'loggedin' in session:
#         print("asdf")
#         Student_id = request.args.get('StudentId') 
#         print(Student_id)
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * from student_attendance WHERE Student_id = %s', (Student_id,))
#         student_attendance = cursor.fetchall() 
        
#         cursor.execute('SELECT * FROM courses')
#         subjects = cursor.fetchall()

#         cursor.execute('SELECT * FROM classes')
#         classes = cursor.fetchall()  
        
#         return render_template("update_attendance.html", student_attendance = student_attendance, subjects = subjects, classes = classes)
#     return redirect(url_for('login')) 

@app.route("/update_attendance", methods =['GET'])
def update_attendance():
    if 'loggedin' in session:
        StudentId = request.args.get('StudentId') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from updateAttendance WHERE StudentId = %s', (StudentId,))
        student_attendance = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM courses')
        subjects = cursor.fetchall()

        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall()  
        
        return render_template("update_attendance.html", student_attendance = student_attendance, subjects = subjects, classes = classes)
    return redirect(url_for('login')) 

# @app.route("/save_attendance", methods=['GET', 'POST'])
# def save_attendance():
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         if request.method == 'POST' and 'StudentId' in request.form and 'Class_id' in request.form \
#                 and 'classteacher' in request.form and 'Date' in request.form and 'Attendance' in request.form:
#             StudentId = request.form['StudentId']
#             Class_id = request.form['Class_id']
#             classteacher = request.form['classteacher']
#             Date = request.form['Date']
#             Attendance = request.form['Attendance']
#             action = request.form['action']

#             if action == 'updateAttendance':
#                 # Update the student_attendance table directly
#                 cursor.execute('UPDATE student_attendance \
#                                 SET Class_id = %s, Class_teacher_id = %s, Date = %s, Attendance = %s \
#                                 WHERE Student_id = %s',
#                                (Class_id, classteacher, Date, Attendance, StudentId))

#                 # Commit the changes
#                 mysql.connection.commit()

#                 return redirect(url_for('studentAttendance'))

#     return redirect(url_for('login'))


@app.route("/save_attendance", methods =['GET', 'POST'])
def save_attendance():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        # currentDate = date.today().strftime('%Y/%m/%d') 
		# if request.method == 'POST' and 'techer_name' in request.form and 'specialization' in request.form:	
		
        if request.method == 'POST' and 'StudentId' in request.form and 'Name' in request.form \
		and 'CoursesTaken' in request.form and 'Class_id' in request.form and 'classteacher' in request.form \
		and 'Department' in request.form and 'Date' in request.form and 'Attendance' in request.form:
            StudentId = request.form['StudentId'] 
            Name = request.form['Name'] 
            CoursesTaken = request.form['CoursesTaken'] 
            Class_id = request.form['Class_id'] 
            classteacher = request.form['classteacher'] 
            Department = request.form['Department'] 
            Date = request.form['Date'] 
            Attendance = request.form['Attendance'] 
            action = request.form['action']             
            
            if action == 'updateAttendance':
                StudentId = request.form['StudentId'] 
                Name = request.form['Name'] 
                CoursesTaken = request.form['CoursesTaken'] 
                Class_id = request.form['Class_id'] 
                classteacher = request.form['classteacher'] 
                Department = request.form['Department'] 
                Date = request.form['Date'] 
                Attendance = request.form['Attendance'] 
                cursor.execute('UPDATE student_attendance SET Class_id = %s, Class_teacher_id = %s, Date = %s, Attendance = %s WHERE Student_id = %s',
                               (Class_id, classteacher, Date, Attendance, (StudentId, ), ))
                # cursor.execute('UPDATE updateAttendance \
                #    SET Name = %s, CoursesTaken = %s, Class_id = %s, classteacher = %s, \
                #    Department = %s, Date = %s, Attendance = %s \
				#     WHERE StudentId =%s', (Name, CoursesTaken, Class_id, classteacher, Department, Date, Attendance, (StudentId, ), ))
                
                # cursor.execute('UPDATE teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))

                mysql.connection.commit()      
            return redirect(url_for('studentAttendance')) 
        # return redirect(url_for('studentAttendance'))                
    return redirect(url_for('login')) 
 
########################### FACULTY ATTENDANCE ##################################

@app.route("/facultyAttendance", methods =['GET', 'POST'])
def facultyAttendance():
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM updateTeacherAttendance')
        faculty_attendance = cursor.fetchall()

        cursor.execute('SELECT * FROM courses')
        subjects = cursor.fetchall() 

        cursor.execute('SELECT * FROM faculty')
        teachers = cursor.fetchall()

        # cursor.execute('SELECT *,concat(FirstName,LastName) as Name FROM students')
        # students = cursor.fetchall()

        return render_template("faculty_attendance.html", teachers = teachers, classes = classes, subjects=subjects, faculty_attendance = faculty_attendance)
    return redirect(url_for('login')) 
    
    
@app.route("/getFacultyAttendance", methods =['GET', 'POST'])
def getFacultyAttendance():
    if 'loggedin' in session:
        print('Started!!')  
        if request.method == 'POST' or 'Teacher_Id' in request.form:
        
            Teacher_Id = request.form['Teacher_Id']
            # StudentId = request.form['StudentId']

            print('Teacher_Id')
            print(Teacher_Id)
            # sectionid = request.form['sectionid']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
            
            cursor.execute('SELECT * FROM classes')
            classes = cursor.fetchall() 

            cursor.execute('SELECT * FROM faculty')
            teachers = cursor.fetchall()
            
            # cursor.execute('SELECT * FROM section')
            # sections = cursor.fetchall() 
            cursor.execute('SELECT * FROM updateTeacherAttendance where Department = %s', (Teacher_Id, ))
            faculty_attendance = cursor.fetchall()

            currentDate = date.today().strftime('%Y/%m/%d')
                     
            # cursor.execute('SELECT s.id, s.name, s.photo, s.gender, s.dob, s.mobile, s.email, s.current_address, s.father_name, s.mother_name,s.admission_no, s.roll_no, s.admission_date, s.academic_year, a.attendance_status, a.attendance_date FROM students as s LEFT JOIN attendance as a ON s.id = a.student_id WHERE s.class = '+classid+' AND s.section = '+sectionid)              
            # cursor.execute('SELECT *,concat(FirstName,LastName) as Name from Students')
            # students = cursor.fetchall()   
                      
            return render_template("faculty_attendance.html", teachers = teachers, classes = classes,  Teacher_Id = Teacher_Id, faculty_attendance = faculty_attendance)        
        elif request.method == 'POST':
            msg = 'Please fill out the form field !'        
        return redirect(url_for('facultyAttendance'))        
    return redirect(url_for('login'))

# @app.route("/update_attendance", methods =['GET'])
# def update_attendance():
#     if 'loggedin' in session:
#         print("asdf")
#         Student_id = request.args.get('StudentId') 
#         print(Student_id)
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * from student_attendance WHERE Student_id = %s', (Student_id,))
#         student_attendance = cursor.fetchall() 
        
#         cursor.execute('SELECT * FROM courses')
#         subjects = cursor.fetchall()

#         cursor.execute('SELECT * FROM classes')
#         classes = cursor.fetchall()  
        
#         return render_template("update_attendance.html", student_attendance = student_attendance, subjects = subjects, classes = classes)
#     return redirect(url_for('login')) 

@app.route("/update_facultyattendance", methods =['GET'])
def update_facultyattendance():
    if 'loggedin' in session:
        Teacher_Id = request.args.get('Teacher_Id') 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from updateTeacherAttendance WHERE Teacher_Id = %s', (Teacher_Id,))
        faculty_attendance = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM courses')
        subjects = cursor.fetchall()

        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall()  
        
        return render_template("update_facultyattendance.html", faculty_attendance = faculty_attendance, subjects = subjects, classes = classes)
    return redirect(url_for('login')) 

# @app.route("/save_attendance", methods=['GET', 'POST'])
# def save_attendance():
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         if request.method == 'POST' and 'StudentId' in request.form and 'Class_id' in request.form \
#                 and 'classteacher' in request.form and 'Date' in request.form and 'Attendance' in request.form:
#             StudentId = request.form['StudentId']
#             Class_id = request.form['Class_id']
#             classteacher = request.form['classteacher']
#             Date = request.form['Date']
#             Attendance = request.form['Attendance']
#             action = request.form['action']

#             if action == 'updateAttendance':
#                 # Update the student_attendance table directly
#                 cursor.execute('UPDATE student_attendance \
#                                 SET Class_id = %s, Class_teacher_id = %s, Date = %s, Attendance = %s \
#                                 WHERE Student_id = %s',
#                                (Class_id, classteacher, Date, Attendance, StudentId))

#                 # Commit the changes
#                 mysql.connection.commit()

#                 return redirect(url_for('studentAttendance'))

#     return redirect(url_for('login'))


@app.route("/save_facultyattendance", methods =['GET', 'POST'])
def save_facultyattendance():
    if 'loggedin' in session:    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        # currentDate = date.today().strftime('%Y/%m/%d') 
		# if request.method == 'POST' and 'techer_name' in request.form and 'specialization' in request.form:	
		
        if request.method == 'POST' and 'Teacher_Id' in request.form and 'Name' in request.form \
		and 'Course_Id' in request.form and 'Class_id' in request.form  \
		and 'Department' in request.form and 'Date' in request.form and 'Attendance' in request.form:
            Teacher_Id = request.form['Teacher_Id'] 
            Name = request.form['Name'] 
            Course_Id = request.form['Course_Id'] 
            Class_id = request.form['Class_id'] 
            # classteacher = request.form['classteacher'] 
            Department = request.form['Department'] 
            Date = request.form['Date'] 
            Attendance = request.form['Attendance'] 
            action = request.form['action']             
            
            if action == 'updateFacultyAttendance':
                Teacher_Id = request.form['Teacher_Id'] 
                Name = request.form['Name'] 
                Course_Id = request.form['Course_Id'] 
                Class_id = request.form['Class_id'] 
                # classteacher = request.form['classteacher'] 
                Department = request.form['Department'] 
                Date = request.form['Date'] 
                Attendance = request.form['Attendance'] 
                cursor.execute('UPDATE faculty_attendance SET Class_id = %s, Department = %s, Date = %s, Attendance = %s WHERE Teacher_Id = %s',
                               (Class_id, Department, Date, Attendance, (Teacher_Id, ), ))
                # cursor.execute('UPDATE updateAttendance \
                #    SET Name = %s, CoursesTaken = %s, Class_id = %s, classteacher = %s, \
                #    Department = %s, Date = %s, Attendance = %s \
				#     WHERE StudentId =%s', (Name, CoursesTaken, Class_id, classteacher, Department, Date, Attendance, (StudentId, ), ))
                
                # cursor.execute('UPDATE teacher SET teacher = %s, subject_id = %s WHERE teacher_id =% s', (techer_name, specialization, (teacherid, ), ))

                mysql.connection.commit()      
            return redirect(url_for('facultyAttendance')) 
        # return redirect(url_for('studentAttendance'))                
    return redirect(url_for('login')) 

##################### REPORT ################################

@app.route("/report", methods =['GET', 'POST'])
def report():
    if 'loggedin' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM classes')
        classes = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM section')
        sections = cursor.fetchall()
        
        return render_template("report.html", classes = classes, sections = sections)
    return redirect(url_for('login'))     
    
if __name__ == "__main__":
    app.run()
    os.execv(__file__, sys.argv)

