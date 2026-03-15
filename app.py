# Importing the modules >>
import os
from flask import Flask,render_template,request,redirect
from pymongo import MongoClient
from bson import ObjectId

# Initialise mongoclient >>
client = MongoClient('mongodb://localhost:27017/')

# Select the Database & Collection >>
db = client.student
collection = db.sinfo

# Find all Student Records 🧑‍🎓 >>
def GetAllStudents():
    cursor = collection.find({})

    students = []

    for i in cursor:
        students.append(i)

    return students

# Creating Flask Application >>
app = Flask(__name__)

# Health Check End Point >>

@app.route("/health")
def health():
    return 'Server is up and running'
    
# Creating Routing for App >>

@app.route("/")
def Home():
    students = GetAllStudents()
    return render_template('home.html',students=students)

#  Add Student Form Data >>>

@app.route("/add",methods=['POST'])
def Add_Data():
    name = request.form['name']
    temp_marks = str(request.form['marks']).split(",")
    dept = request.form['dept']

    marks = [float(x) for x in temp_marks]

    student = {'name': name,'marks': marks,'dept':dept}

    collection.insert_one(student)

    return redirect("/")

# Delete Student Data  >>

@app.route('/delete/<id>')
def delete_student(id):
    # delete the student record with the given id from the collection
    collection.delete_one({'_id': ObjectId(id)})
    # redirect the user back to the home page
    return redirect('/')


@app.route('/update/<id>', methods=['GET', 'POST'])
def get_update_student(id):
    update_student = collection.find_one({'_id':ObjectId(id)})

    print(update_student)

    students = GetAllStudents()
    return render_template('home.html',students=students,update_student=update_student)


@app.route('/update', methods=['POST'])
def update_student():
    # Get the student ID from the form data
    id = request.form['id']
    
    # Find the student with the given ID
    student = collection.find_one({'_id':ObjectId(id)})

    if student:
        # Update the student data with the form data
        name = request.form['name']
        dept = request.form['dept']
        
        temp_marks = str(request.form['marks'])[1:-1].split(",")
        marks = [ float(i) for i in temp_marks ]
        
        collection.update_one({'_id': ObjectId(id)}, {"$set": {'name': name, 'dept': dept, 'marks': marks}})



        return redirect("/")
    else:
        return 'Student not found'

#  Run the application >>
if __name__ == '__main__':
    # Use environment variables with safe defaults
    debug_mode = os.getenv('FLASK_DEBUG', 'True')
    host_ip = os.getenv('FLASK_RUN_HOST', '0.0.0.0') 
    
    app.run(debug=debug_mode, host=host_ip, port=5000)
