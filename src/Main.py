# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "home"
__date__ = "$26 Apr, 2021 6:30:58 PM$"

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import numpy as np
import os
import pandas as pd
import pygal
import pymysql
import random
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy import create_engine
import urllib.parse as urlparse
from urllib.parse import parse_qs
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = "1234"
app.password = ""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "sociamedia"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def getuserprofiledetails(self, username):
        strQuery = "SELECT PersonId,Firstname,Lastname,Phoneno,DOB,Age,Address,Recorded_Date FROM personaldetails WHERE Username = '" + username + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertdoctordetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertdoctordetails::' + username)
        strQuery = "INSERT INTO doctordetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def inserthistorydetails(self, PersonId, Question1Id, Question2Id, Question3Id, Question4Id, Question5Id, Question6Id, Result, Percentage):
        print('inserthistorydetails::' + str(PersonId))
        strQuery = "INSERT INTO historydetails(PersonId, Question1Id, Question2Id, Question3Id, Question4Id, Question5Id, Question6Id, Result, Percentage, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (str(PersonId), Question1Id, Question2Id, Question3Id, Question4Id, Question5Id, Question6Id, Result, Percentage)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertpersonaldetails(self, firstname, lastname, phone, dob, age, email, address, username, password):
        print('insertpersonaldetails::' + username)
        strQuery = "INSERT INTO personaldetails(Firstname, Lastname, Phoneno, DOB, Age, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, dob, age, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatepersonaldetails(self, PersonId, firstname, lastname, phone, dob, age, email, address):
        print('updatepersonaldetails::' + str(PersonId))
        strQuery = "UPDATE personaldetails SET Firstname = '" + str(firstname) + "', Lastname = '" + str(lastname) + "', Phoneno = '" + str(phone) + "', DOB = '" + str(dob) + "', Age = '" + str(age) + "', Emailid = '" + str(email) + "', Address = '" + str(address) + "' WHERE PersonId = '" + str(PersonId) + "' "
        self.cur.execute(strQuery)
        self.con.commit()
        return ""
    def insertquerydetails(self, PersonId, DoctorId, Comments):
        print('insertquerydetails::' + Comments)
        strQuery = "INSERT INTO querydetails(PersonId, DoctorId, Comments, Reply, Recorded_Date) values(%s, %s, %s, '-', now())"
        strQueryVal = (PersonId, DoctorId, Comments)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatequerydetails(self, queryId, Comments):
        print('updatequerydetails::' + queryId)
        strQuery = "UPDATE querydetails SET Reply = '" + Comments + "' WHERE QueryId = '" + queryId + "' "
        self.cur.execute(strQuery)
        self.con.commit()
        return ""
    def getpersonaldetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, PersonId FROM personaldetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getdoctorlogindetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, DoctorId FROM doctordetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getuserpersonaldetails(self, name):
        strQuery = "SELECT PersonId, Firstname, Lastname, Phoneno, DOB, Age, Emailid, Address, Recorded_Date FROM personaldetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getquerydetails(self, PersonId):
        strQuery = "SELECT d.Firstname, d.Lastname, q.Comments, q.Reply, q.Recorded_Date FROM querydetails AS q LEFT JOIN doctordetails AS d ON d.DoctorId = q.DoctorId WHERE q.PersonId = '" + str(PersonId) + "' ORDER BY Recorded_Date DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdoctorquerydetails(self, DoctorId):
        strQuery = "SELECT p.Firstname, p.Lastname, q.QueryId, q.Comments, q.Reply, q.Recorded_Date FROM querydetails AS q LEFT JOIN personaldetails AS p ON p.PersonId = q.PersonId WHERE q.DoctorId = '" + str(DoctorId) + "' ORDER BY Recorded_Date DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getvideodetails(self):
        strQuery = "SELECT v.VideoId, v.VideoUrl, c.Name, v.Recorded_Date FROM videodetails AS v LEFT JOIN categorydetails AS c ON c.CategoryId = v.CategoryId "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result    
    def getdoctordetails(self, name):
        strQuery = "SELECT DoctorId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM doctordetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdoctorlistdetails(self):
        strQuery = "SELECT DoctorId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM doctordetails LIMIT 10 "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result		
    def getuseranswerdetails(self, PersonId):
        strQuery = "SELECT ua.UserAnswerId, q.Question, ua.Answer, ua.Recorded_Date FROM useranswerdetails AS ua LEFT JOIN questiondetails AS q ON q.QuestionId = ua.QuestionId WHERE ua.PersonId = '" + str(PersonId) + "' AND ua.QuestionId IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19) GROUP BY ua.QuestionId ORDER BY Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getuseranswerdetailsbyquestionid(self, PersonId, QuestionId):
        strQuery = "SELECT ua.QuestionId, ua.Answer FROM useranswerdetails AS ua WHERE ua.PersonId = '" + str(PersonId) + "' AND ua.QuestionId IN ('" + str(QuestionId) + "') GROUP BY ua.QuestionId ORDER BY Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getstressdetails(self, id):
        strQuery = "SELECT StressId, Name, Recorded_Date FROM stressdetails WHERE StressId = '" + str(id) + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getanswerdetails(self, Answer, QuestionId):
        strQuery = "SELECT AnswerId, Answer, Category, Recorded_Date FROM answerdetails WHERE Answer = '" + str(Answer) + "' AND QuestionId = '" + str(QuestionId) + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertsurveydataset(self, PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19):
        print('insertsurveydataset::' + Email_Address)
        strQuery = "INSERT INTO surverydataset(PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return "" 
    def insertuseranswerdetails(self, PersonId, q1, a1):
        print('insertuseranswerdetails::' + str(PersonId))
        strQuery = "INSERT INTO useranswerdetails(PersonId, QuestionId, Answer, Recorded_Date) values(%s, %s, %s, now())"
        strQueryVal = (PersonId, q1, a1)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return "" 
    def deleteuseranswerdetails(self, PersonId):
        print('deleteuseranswerdetails::' + str(PersonId))
        strQuery = "DELETE FROM useranswerdetails WHERE PersonId = (%s) " 
        strQueryVal = (str(PersonId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def deletesurveydataset(self, loanId):
        print(loanId)
        strQuery = "DELETE FROM surverydataset WHERE Sno = (%s) " 
        strQueryVal = (str(loanId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def getsurveydatasetuploadeddetails(self):
        strQuery = "SELECT Sno, PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Recorded_Date "
        strQuery += "FROM surverydataset "
        strQuery += "ORDER BY Sno DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getgraphdetails(self, dataownername):
        strQuery = "SELECT COUNT(*) AS c, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Attack "        
        strQuery += "FROM kdddataset "        
        strQuery += "GROUP BY Protocol, Service, Flag, Attack "   
        print(strQuery)
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getallprotocoldetails(self):
        strQuery = "SELECT DISTINCT(Protocol) AS Protocol FROM kdddataset"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getkdddatasetdatabyname(self, protocol):
        strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
        strQuery += "FROM kdddataset "
        strQuery += "WHERE Protocol = '" + protocol + "'  "
        strQuery += "ORDER BY Sno DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertanalysisdetails(self, Accuracy, Algorithm):
        print('insertanalysisdetails::' + Algorithm)
        strQuery = "INSERT INTO analysisdetails(Accuracy, Algorithm, Recorded_Date) values(%s, %s, now())"
        strQueryVal = (str(Accuracy).encode('utf-8', 'ignore'), str(Algorithm).encode('utf-8', 'ignore'))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""  
    def getallknndetails(self):
        strQuery = "SELECT sum(Accuracy) as c FROM analysisdetails WHERE Algorithm = 'KNN'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result  
    def gettaskdetails(self, offset, limit):
        strQuery = "SELECT TaskId, TaskName, Recorded_Date FROM taskdetails LIMIT %s OFFSET %s"        
        strQueryVal = (limit, offset)
        self.cur.execute(strQuery, strQueryVal)        
        result = self.cur.fetchall()
        print(result)
        return result
    def gethistorydetails(self, PersonId):
        strQuery = "SELECT h.HistoryId, h.PersonId, (SELECT Answer FROM answerdetails WHERE QuestionId = 1 AND Category = h.Question1Id) AS Answer1, "        
        strQuery += "(SELECT Answer FROM answerdetails WHERE QuestionId = 2 AND Category = h.Question1Id) AS Answer2, " 
        strQuery += "(SELECT Answer FROM answerdetails WHERE QuestionId = 3 AND Category = h.Question1Id) AS Answer3, "        
        strQuery += "(SELECT Answer FROM answerdetails WHERE QuestionId = 4 AND Category = h.Question1Id) AS Answer4, "        
        strQuery += "(SELECT Answer FROM answerdetails WHERE QuestionId = 5 AND Category = h.Question1Id) AS Answer5, "        
        strQuery += "(SELECT Answer FROM answerdetails WHERE QuestionId = 6 AND Category = h.Question1Id) AS Answer6, "   
        strQuery += "Result, Percentage, Recorded_Date "      
        strQuery += "FROM historydetails AS h "    
        strQuery += "WHERE h.PersonId = '" + str(PersonId) + "'  "
        strQuery += "ORDER BY h.HistoryId DESC "    
        strQuery += "LIMIT 10 "    
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()
        print(result)
        return result
    def getallkmeansdetails(self):
        strQuery = "SELECT sum(Accuracy) as c FROM analysisdetails WHERE Algorithm = 'K-Means'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    
@app.route('/', methods=['GET'])
def loadindexpage():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/codeindex', methods=['POST'])
def codeindex():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['PersonId'];
                    def db_query():
                        db = Database()
                        emps = db.getuserprofiledetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('index.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('index.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('index.html')
        
    return render_template('index.html')

@app.route('/usersignin', methods=['GET'])
def usersignin():
    return render_template('usersignin.html')

@app.route('/codeusersignin', methods=['POST'])
def codeusersignin():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    dob = request.form['datepicker1']
    age = request.form['age']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('dob:', dob)
    print('age:', age)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and phone is not ""  and dob is not "" and age is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('usersignin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertpersonaldetails(firstname, lastname, phone, dob, age, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('index.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('usersignin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('usersignin.html')
    
    return render_template('usersignin.html')

@app.route('/userprofile', methods=['GET'])
def userprofile():
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/signout', methods=['GET'])
def signout():    
    return render_template('signout.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['x']
    return render_template('index.html')

@app.route('/uploaddata', methods=['GET'])
def uploaddata():
    return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codeuploaddata', methods=['POST'])
def codeuploaddata(): 
    file = request.files['filepath']
    
    print('filename:' + file.filename)
       
    if 'filepath' not in request.files:
        flash ('Please fill all mandatory fields.')
        return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')
    
    if file.filename != '':

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = UPLOAD_FOLDER + "/" + file.filename

            print('filepath:' + filepath)
            
            data = pd.read_csv(filepath)
            
            # print info about columns in the dataframe 
            print(data.info()) 
            
            # Dropped all the Null, Empty, NA values from csv file 
            csvrows = data.dropna(axis=0, how='any') 

            count = len(csvrows);
            
            print('Length of Data::', count)

            for i in range(count): 
                
                if i == 0:
                    print(count)
                    
                else:  
                    db = Database()
                    db.insertsurveydataset(session['UID'], str(np.array(csvrows['Timestamp'])[i]), str(np.array(csvrows['Email_Address'])[i]), str(np.array(csvrows['Name'])[i]), str(np.array(csvrows['Q1'])[i]), str(np.array(csvrows['Q2'])[i]), str(np.array(csvrows['Q3'])[i]), str(np.array(csvrows['Q4'])[i]), str(np.array(csvrows['Q5'])[i]), str(np.array(csvrows['Q6'])[i]), str(np.array(csvrows['Q7'])[i]), str(np.array(csvrows['Q8'])[i]), str(np.array(csvrows['Q9'])[i]), str(np.array(csvrows['Q10'])[i]), str(np.array(csvrows['Q11'])[i]), str(np.array(csvrows['Q12'])[i]), str(np.array(csvrows['Q13'])[i]), str(np.array(csvrows['Q14'])[i]), str(np.array(csvrows['Q15'])[i]), str(np.array(csvrows['Q16'])[i]), str(np.array(csvrows['Q17'])[i]), str(np.array(csvrows['Q18'])[i]), str(np.array(csvrows['Q19'])[i])) 

            flash('File successfully uploaded!')
            return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

        else:
            flash('Allowed file types are .txt')
            return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')
    else:
        flash ('Please fill all mandatory fields.')           
        return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route('/viewuploadeddata', methods=['GET'])
def viewuploadeddata():
    def db_query():
        db = Database()
        emps = db.getsurveydatasetuploadeddetails()       
        return emps
    profile_res = db_query()
    return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/deletedata', methods=['GET'])
def deletedata():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    loanId = parse_qs(parsed.query)['index']
    print(loanId)
    
    try:
        if loanId is not "": 
            
            db = Database()
            db.deletesurveydataset(loanId[0])
            
            def db_query():
                db = Database()
                emps = db.getsurveydatasetuploadeddetails()    
                return emps
            profile_res = db_query()
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/graph', methods=['GET'])
def graph():
    
    def accepteddb_query():
        db = Database()
        emps = db.getgraphdetails(session['x'])       
        return emps
    res = accepteddb_query()
    
    graph = pygal.Line()
    
    graph.title = '% Comparison Graph Between Attacks vs Number of Counts.'
    
    graph.x_labels = ['c', 'de_bytes', 'nc_bytes']
    
    for row in res:
        
        print(row['c'])
        
        graph.add(row['Protocol'] + '-' + row['Service'] + '-' + row['Flag'] + '-' + row['Attack'], [int(row['c']), int(row['de_bytes']), int(row['nc_bytes'])])
        
    graph_data = graph.render_data_uri()
    
    return render_template('graph.html', sessionValue=session['x'], graph_data=graph_data)

@app.route('/searchknn', methods=['GET'])
def searchknn():    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    return render_template('searchknn.html', sessionValue=session['x'], protocolresult=protocolresult, content_type='application/json')

@app.route('/codesearchknn', methods=['POST'])
def codesearchknn():  
    
    protocolname = request.form['protocol']
    
    print('protocolname:' + protocolname)
    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    
    try:
        if protocolname is not "": 
            
            db_connection_str = 'mysql+pymysql://root:' + app.password + '@localhost/anomalydetection?charset=utf8'
            
            db_connection = create_engine(db_connection_str)

            strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
            strQuery += "FROM kdddataset "
            strQuery += "WHERE Protocol = '" + protocolname + "'  "
            strQuery += "ORDER BY Sno DESC "
            strQuery += "LIMIT 10" 
            
            print('Query::', strQuery)
        
            df = pd.read_sql(strQuery, con=db_connection)

            # you want all rows, and the feature_cols' columns
            X = df.iloc[:, 8: 42].values
            y = df.iloc[:, 5: 6].values

            print('X Data::', X)

            # Split into training and test set 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

            knn = KNeighborsClassifier(n_neighbors=7) 

            knn.fit(X_train, y_train) 

            # Predict on dataset which model has not seen before 
            y_knn = knn.predict(X_test);

            result = metrics.accuracy_score(y_test, y_knn)

            print("KNN Accuracy :", result); 
            
            algo = 'KNN'
            
            db = Database()
            db.insertanalysisdetails(result, algo) 
            
            def db_query():
                db = Database()
                emps = db.getkdddatasetdatabyname(protocolname)
                return emps
            profile_res = db_query()
            
            return render_template('codesearchknn.html', sessionValue=session['x'], result=profile_res, protocolresult=protocolresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchknn.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchknn.html', sessionValue=session['x'])
    
    return render_template('searchknn.html', sessionValue=session['x'])

@app.route('/searchkmeans', methods=['GET'])
def searchkmeans():    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    return render_template('searchkmeans.html', sessionValue=session['x'], protocolresult=protocolresult, content_type='application/json')

@app.route('/codesearchkmeans', methods=['POST'])
def codesearchkmeans():  
    
    protocolname = request.form['protocol']
    
    print('protocolname:' + protocolname)
    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    
    try:
        if protocolname is not "": 
            
            db_connection_str = 'mysql+pymysql://root:' + app.password + '@localhost/anomalydetection?charset=utf8'
            
            db_connection = create_engine(db_connection_str)

            strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
            strQuery += "FROM kdddataset "
            strQuery += "WHERE Protocol = '" + protocolname + "'  "
            strQuery += "ORDER BY Sno DESC "
            strQuery += "LIMIT 10" 
            
            print('Query::', strQuery)
        
            df = pd.read_sql(strQuery, con=db_connection)

            # you want all rows, and the feature_cols' columns
            X = df.iloc[:, 8: 42].values
            y = df.iloc[:, 5: 6].values

            print('X Data::', X)

            kmeans = KMeans(n_clusters=4)
            kmeans.fit(X)

            y_kmeans = kmeans.predict(X)
            
            print("y_kmeans :", y_kmeans); 
            
            result = y_kmeans[0] * 2
            
            algo = 'K-Means'
            
            print("K-Means Accuracy :", result); 
            
            db = Database()
            db.insertanalysisdetails(result, algo) 
            
            def db_query2():
                db = Database()
                emps = db.getkdddatasetdatabyname(protocolname)
                return emps
            profile_res = db_query2()
            
            return render_template('codesearchkmeans.html', sessionValue=session['x'], result=profile_res, protocolresult=protocolresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchkmeans.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchkmeans.html', sessionValue=session['x'])
    
    return render_template('searchkmeans.html', sessionValue=session['x'])

@app.route('/comparisongraph', methods=['GET'])
def comparisongraph():
    
    labels = ["KNN ALGORITHM", "K-MEANS ALGORITHM"]
    
    def kmeans_query():
        db = Database()
        emps = db.getallkmeansdetails()       
        return emps
    res = kmeans_query()

    kmeanscount = 0;

    for row in res:
        print(row['c'])
        kmeanscount = row['c']
        
    def knn_query():
        db = Database()
        emps = db.getallknndetails()       
        return emps
    res = knn_query()

    knncount = 0;

    for row in res:
        print(row['c'])
        knncount = row['c']
        
    values = [knncount, kmeanscount]

    return render_template('comparisongraph.html', sessionValue=session['x'], values=values, labels=labels)

@app.route('/quiz', methods=['GET'])
def quiz():
    return render_template('quiz.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz', methods=['POST'])
def codequiz():
    db = Database()
    db.deleteuseranswerdetails(session['UID'])    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_1', methods=['POST'])
def quiz_1():    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_1', methods=['POST'])
def codequiz_1():
    q1 = request.form['one']
    q2 = request.form['two']
    a1 = request.form['a']
    a2 = request.form['b']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_2', methods=['POST'])
def quiz_2():
    return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_2', methods=['POST'])
def codequiz_2():
    q1 = request.form['three']
    q2 = request.form['four']
    a1 = request.form['c']
    a2 = request.form['d']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_3', methods=['POST'])
def quiz_3():
    return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_3', methods=['POST'])
def codequiz_3():
    q1 = request.form['five']
    q2 = request.form['six']
    a1 = request.form['e']
    a2 = request.form['f']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return redirect(url_for("results"))
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')

@app.route('/results', methods=['GET'])
def results():
        
    #Load the data-set
    dataset = pd.read_csv('C:/Dataset/MediaSurvey.csv') 

    #Print the count of rows and coulmns in csv file
    print("Dimensions of Dataset: {}".format(dataset.shape))

    # Dropped all the Null, Empty, NA values from csv file 
    new_dataset = dataset.dropna(axis=0, how='any') 

    print("Dimensions of Dataset after Pre-processing : {}".format(new_dataset.shape))

    #Encoding categorical data values
    from sklearn.preprocessing import LabelEncoder

    labelencoder_Y = LabelEncoder()
    
    
    #Data conversion for Url Column
    filter_dataset_answer = dataset.drop_duplicates(subset=["Q1"])

    print("Dimensions of Dataset after Filtering : {}".format(filter_dataset_answer.shape))

    c = filter_dataset_answer.iloc[:, 3:4];

    answer_types = ();
    answer_types = list(answer_types)

    for i in range(len(c)):
        answer_types.append(c.values[i]);

    answer_types = tuple(answer_types)

    print("answer_types: ", answer_types)

    filter_dataset_answer_types = pd.DataFrame(answer_types, columns=['Q1_Answer'])

    # creating instance of labelencoder
    labelencoder = LabelEncoder()

    # Assigning numerical values and storing in another column
    filter_dataset_answer_types['Q1_Answer_Category'] = labelencoder.fit_transform(filter_dataset_answer_types['Q1_Answer'])

    print("filter_dataset_answer_types: ", filter_dataset_answer_types);

    filter_dataset_answer_types.to_csv('C:/Dataset/Q1_Answer.csv', encoding='utf-8')
    
            
    #Data conversion for Url Column
    filter_dataset_answer1 = dataset.drop_duplicates(subset=["Q2"])

    print("Dimensions of Dataset after Filtering : {}".format(filter_dataset_answer1.shape))

    c = filter_dataset_answer1.iloc[:, 4:5];

    answer1_types = ();
    answer1_types = list(answer1_types)

    for i in range(len(c)):
        answer1_types.append(c.values[i]);

    answer1_types = tuple(answer1_types)

    print("answer1_types: ", answer1_types)

    filter_dataset_answer1_types = pd.DataFrame(answer1_types, columns=['Q2_Answer'])

    # creating instance of labelencoder
    labelencoder = LabelEncoder()

    # Assigning numerical values and storing in another column
    filter_dataset_answer1_types['Q2_Answer_Category'] = labelencoder.fit_transform(filter_dataset_answer1_types['Q2_Answer'])

    print("filter_dataset_answer_types: ", filter_dataset_answer1_types);

    filter_dataset_answer1_types.to_csv('C:/Dataset/Q2_Answer.csv', encoding='utf-8')
    
        
    #Data conversion for Url Column
    filter_dataset_answer2 = dataset.drop_duplicates(subset=["Q3"])

    print("Dimensions of Dataset after Filtering : {}".format(filter_dataset_answer2.shape))

    c = filter_dataset_answer2.iloc[:, 5:6];

    answer2_types = ();
    answer2_types = list(answer2_types)

    for i in range(len(c)):
        answer2_types.append(c.values[i]);

    answer2_types = tuple(answer2_types)

    print("answer2_types: ", answer2_types)

    filter_dataset_answer2_types = pd.DataFrame(answer2_types, columns=['Q3_Answer'])

    # creating instance of labelencoder
    labelencoder = LabelEncoder()

    # Assigning numerical values and storing in another column
    filter_dataset_answer2_types['Q3_Answer_Category'] = labelencoder.fit_transform(filter_dataset_answer2_types['Q3_Answer'])

    print("filter_dataset_answer_types: ", filter_dataset_answer2_types);

    filter_dataset_answer2_types.to_csv('C:/Dataset/Q3_Answer.csv', encoding='utf-8')
    
        
    #Data conversion for Url Column
    filter_dataset_answer3 = dataset.drop_duplicates(subset=["Q4"])

    print("Dimensions of Dataset after Filtering : {}".format(filter_dataset_answer3.shape))

    c = filter_dataset_answer3.iloc[:, 6:7];

    answer3_types = ();
    answer3_types = list(answer3_types)

    for i in range(len(c)):
        answer3_types.append(c.values[i]);

    answer3_types = tuple(answer3_types)

    print("answer3_types: ", answer3_types)

    filter_dataset_answer3_types = pd.DataFrame(answer3_types, columns=['Q4_Answer'])

    # creating instance of labelencoder
    labelencoder = LabelEncoder()

    # Assigning numerical values and storing in another column
    filter_dataset_answer3_types['Q4_Answer_Category'] = labelencoder.fit_transform(filter_dataset_answer3_types['Q4_Answer'])

    print("filter_dataset_answer_types: ", filter_dataset_answer3_types);

    filter_dataset_answer3_types.to_csv('C:/Dataset/Q4_Answer.csv', encoding='utf-8')
    
    
    #Data conversion for Url Column
    filter_dataset_answer4 = dataset.drop_duplicates(subset=["Q5"])

    print("Dimensions of Dataset after Filtering : {}".format(filter_dataset_answer4.shape))

    c = filter_dataset_answer4.iloc[:, 7:8];

    answer4_types = ();
    answer4_types = list(answer4_types)

    for i in range(len(c)):
        answer4_types.append(c.values[i]);

    answer4_types = tuple(answer4_types)

    print("answer4_types: ", answer4_types)

    filter_dataset_answer4_types = pd.DataFrame(answer4_types, columns=['Q5_Answer'])

    # creating instance of labelencoder
    labelencoder = LabelEncoder()

    # Assigning numerical values and storing in another column
    filter_dataset_answer4_types['Q5_Answer_Category'] = labelencoder.fit_transform(filter_dataset_answer4_types['Q5_Answer'])

    print("filter_dataset_answer4_types: ", filter_dataset_answer4_types);

    filter_dataset_answer4_types.to_csv('C:/Dataset/Q5_Answer.csv', encoding='utf-8')
        
    #Data conversion for Url Column
    filter_dataset_answer5 = dataset.drop_duplicates(subset=["Q6"])

    print("Dimensions of Dataset after Filtering : {}".format(filter_dataset_answer5.shape))

    c = filter_dataset_answer5.iloc[:, 8:9];

    answer5_types = ();
    answer5_types = list(answer5_types)

    for i in range(len(c)):
        answer5_types.append(c.values[i]);

    answer5_types = tuple(answer5_types)

    print("answer5_types: ", answer5_types)

    filter_dataset_answer5_types = pd.DataFrame(answer5_types, columns=['Q6_Answer'])

    # creating instance of labelencoder
    labelencoder = LabelEncoder()

    # Assigning numerical values and storing in another column
    filter_dataset_answer5_types['Q6_Answer_Category'] = labelencoder.fit_transform(filter_dataset_answer5_types['Q6_Answer'])

    print("filter_dataset_answer5_types: ", filter_dataset_answer5_types);

    filter_dataset_answer5_types.to_csv('C:/Dataset/Q6_Answer.csv', encoding='utf-8')
         
    
    dataset.iloc[:, 3] = labelencoder_Y.fit_transform(dataset.iloc[:, 3].values)

    #print("Encoding : {}".format(labelencoder_Y.fit_transform(dataset.iloc[:, 3].values)));

    dataset.iloc[:, 4] = labelencoder_Y.fit_transform(dataset.iloc[:, 4].values)

    #print("Encoding : {}".format(labelencoder_Y.fit_transform(dataset.iloc[:, 4].values)));

    dataset.iloc[:, 5] = labelencoder_Y.fit_transform(dataset.iloc[:, 5].values)

    #print("Encoding : {}".format(labelencoder_Y.fit_transform(dataset.iloc[:, 5].values)));
    
    dataset.iloc[:, 6] = labelencoder_Y.fit_transform(dataset.iloc[:, 6].values)

    #print("Encoding : {}".format(labelencoder_Y.fit_transform(dataset.iloc[:, 6].values)));
    
    dataset.iloc[:, 7] = labelencoder_Y.fit_transform(dataset.iloc[:, 7].values)

    #print("Encoding : {}".format(labelencoder_Y.fit_transform(dataset.iloc[:, 7].values)));
    
    dataset.iloc[:, 8] = labelencoder_Y.fit_transform(dataset.iloc[:, 8].values)

    #print("Encoding : {}".format(labelencoder_Y.fit_transform(dataset.iloc[:, 8].values)));
            
    X = dataset.iloc[:, 3:9].values
    y = dataset.iloc[:, 9:10].values
    
    # Import train_test_split function
    from sklearn.model_selection import train_test_split

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=109) # 70% training and 30% test

    # linear regression for multioutput regression
    from sklearn.datasets import make_regression
    from sklearn.linear_model import LinearRegression
    
    # define model
    model = LinearRegression()
    
    # fit model
    model.fit(X_train, y_train)
    
    def db_query(answer, QuestionId):
        
        db = Database()
        emps = db.getanswerdetails(answer, QuestionId)  
        
        answer = ''
        for row in emps:
            answer = row['Category']
            
        return answer
        
    def getUserAnswers(QuestionId):
        db = Database()
        emps = db.getuseranswerdetailsbyquestionid(session['UID'], QuestionId) 
        
        answer = ''
        for row in emps:
            answer = row['Answer']
            
        return answer
    
    #print("Answer : {}".format(getUserAnswers(1)));
    
    # make a prediction
    row = [db_query(getUserAnswers(1), 1), db_query(getUserAnswers(2), 2), db_query(getUserAnswers(3), 3), db_query(getUserAnswers(4), 4), db_query(getUserAnswers(5), 5), db_query(getUserAnswers(6), 6)]
    
    print("Row : {}".format(row));
    
    y_pred = model.predict([row])
    
    # summarize prediction
    print(y_pred[0])
    
    value = np.float32(y_pred[0]);
    value = round(value[0], 2) * 100
    value = round(value, 2)
    value1 = round(random.uniform(1, value), 2);
    value2 = round(random.uniform(1, value), 2);
    value3 = round(random.uniform(1, value), 2);
    value4 = round(random.uniform(1, value), 2);
    
    print(value)
    
    results = 'No'
      
    if ((float(value) >= 0) & (float(value) < 50)):
        results = 'Depression'
    elif ((float(value) >= 70) & (float(value) < 75)):
        results = 'Sad'
    elif ((float(value) >= 75) & (float(value) < 80)):
        results = 'Cool'
    elif ((float(value) >= 80) & (float(value) < 90)):
        results = 'Happy'
    else:
        results = 'Angry'
    
    def db_query2():
        db = Database()
        emps = db.inserthistorydetails(session['UID'], db_query(getUserAnswers(1), 1), db_query(getUserAnswers(2), 2), db_query(getUserAnswers(3), 3), db_query(getUserAnswers(4), 4), db_query(getUserAnswers(5), 5), db_query(getUserAnswers(6), 6), results, value)    
        return emps
    res2 = db_query2()
            
    def db_query():
        db = Database()
        emps = db.getuseranswerdetails(session['UID'])       
        return emps
    profile_res = db_query()
    return render_template('results.html', sessionValue=session['x'], result=profile_res, result_1=results, result_2=value, result_3=value1, result_4=value2, result_5=value3, result_6=value4, content_type='application/json')

@app.route('/editprofile', methods=['GET'])
def editprofile():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    queryId = parse_qs(parsed.query)['index']
    queryId = queryId[0]
    print(queryId)
    
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    
    try:
        if queryId is not "":           
            return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('profile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('profile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    
@app.route('/codeeditprofile', methods=['POST'])
def codeeditprofile():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    dob = request.form['datepicker1']
    age = request.form['age']
    email = request.form['email']
    address = request.form['address']      
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('dob:', dob)
    print('age:' + age)    
  
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
            
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and dob is not "" and age is not "" and email is not "" and address is not "": 
            
            db = Database()                
            db.updatepersonaldetails(session['UID'], firstname, lastname, phone, dob, age, email, address);
    
            flash ('Dear Customer, Your details has been updated successfully.')
            return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')                                                   
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    
    return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
	
@app.route('/viewtask', methods=['GET'])
def viewtask():
    
    def db_query():
        db = Database()
        emps = db.gettaskdetails(round(random.uniform(1, 10)), 4)       
        return emps
    profile_res = db_query()
    
    return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/history', methods=['GET'])
def history():
    
    def db_query():
        db = Database()
        emps = db.gethistorydetails(session['UID'])       
        return emps
    profile_res = db_query()
    
    return render_template('history.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
