from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, FIT2101Student, FIT2101Rubric
from forms import LoginForm, SignupForm, EnrollForm



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zmbecnmseaboot:dd4459daa1a19c28aa3b6cbf3f9574bba805cd67f08fda71a30647e71b798f1a@ec2-54-235-102-25.compute-1.amazonaws.com:5432/ddqe9v9b3kauuf'
db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
    session['email'] = None
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)

        else:
            email = form.email.data
            password = form.password.data

            # Get user from the databases
            user = User.query.filter_by(email=email).first()

            if user is not None and user.password == password and user.role == 'L':     # If the user is lecturer
                session['email'] = email
                return redirect(url_for('Lec_pageV2'))

            elif user is not None and user.password == password and user.role == 'D':   # If the user is demonstrator
                session['email'] = email
                return redirect(url_for('dem_page'))

            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route("/signup", methods=["GET","POST"])
def signup():

    form = SignupForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:

            newuser = User(form.first_name.data, form.last_name.data, form.email.data, 'D', form.password.data, form.classes.data, 'fit2101');
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('Lec_pageV2'))

    elif request.method == "GET":
        return render_template('signup.html', form=form)


@app.route("/addRubric", methods=["GET", "POST"])
def addRubric():
    # Get user details
    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role

    if request.method == "POST":

        criteria = request.form['column1']
        poor = request.form['column2']
        satisfactory = request.form['column3']
        good = request.form['column4']
        totalMarks = request.form['column5']
        assessment = request.form['ass_select']
        # Empty relaod page
        if criteria == '' or poor == '' or satisfactory == '' or good == '' or totalMarks == '':
            return redirect(url_for("addRubric"))

        # add row of rubric
        newrow = FIT2101Rubric(criteria, poor, satisfactory, good, totalMarks, assessment)
        db.session.add(newrow)
        db.session.commit()

        if request.form['submit'] == "Add More":
            return render_template("Addrubric.html", user = userrole)
        else:
            return render_template("Lec-pageV2.html")


    return render_template("Addrubric.html", user = userrole)



@app.route("/enrollstd", methods=["GET","POST"])
def enrollstd():
    form = EnrollForm()
    if request.method == "POST":

        if form.validate() == False:
            return render_template('enrollstd.html', form=form)
        else:

            newstudent = FIT2101Student(form.first_name.data, form.last_name.data, form.email.data, form.classes.data)
            db.session.add(newstudent)
            db.session.commit()

            return redirect(url_for('Lec_pageV2'))

    elif request.method == "GET":
        return render_template('enrollstd.html', form=form)


@app.route("/dem-page", methods=["GET", "POST"])
def dem_page():
    if request.method == "POST":

        if request.form["AddGroup"] == 'AddGroup':
            return redirect(url_for('addgroup'))

    email = session['email']
    user = User.query.filter_by(email=email).first()
    nameDem = user.firstname
    return render_template("dem-page.html", name = nameDem)


@app.route("/Lec-pageV2", methods=["GET", "POST"])
def Lec_pageV2():
    if request.method == "POST":
        return redirect(url_for('addgroup'))

    email = session['email']
    user = User.query.filter_by(email=email).first()
    nameDem = user.firstname + " " + user.lastname

    # If nothing in session, then return to index page
    if session['email'] is None:
        return redirect(url_for('index'))

    return render_template("Lec-pageV2.html", name = nameDem)


@app.route("/selectassess", methods=["GET", "POST"])
def selectassess():
    # Get user details
    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role


    studentemail = session['student']
    markstudent = FIT2101Student.query.filter_by(email=studentemail).first()
    if request.method == "POST":
        session['assessment'] = request.form['Ass']
        return redirect(url_for('markstudent'))


    return render_template('selectAssess.html', markStudent = markstudent, user = userrole)



@app.route("/ViewStudents_Dem", methods=["GET", "POST"])
def ViewStudents_Dem():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role

    if request.method == 'POST':
        session['student'] = request.form['Mark']
        return redirect(url_for("selectassess"))

    elif request.method == 'GET':
        email = session['email']
        user = User.query.filter_by(email=email).first()

        # Displaying Students:
        if user.role == 'D':
            stu_classes = user.classes
            listOfStudents = []
            students_list = FIT2101Student.query.all()
            for i in students_list:
                if i.classes == stu_classes:
                    listOfStudents.append(i)

            stu_classes = 'Class ' + str(user.classes)

        elif user.role == 'L':
            listOfStudents = FIT2101Student.query.all()
            stu_classes = 'Lecturer'

        return render_template("ViewStudents_Dem.html", students = listOfStudents, requiredClass = stu_classes, user = userrole)


@app.route("/markstudent", methods=["GET","POST"])
def markstudent():
    # Get user detials
    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role
    # Student in Session['student'] gives the email!!!
    email = session['student']
    student = FIT2101Student.query.filter_by(email=email).first()
    assignment = session['assessment']
    rubrics = []
    listOfRubrics = FIT2101Rubric.query.all()
    for item in listOfRubrics:
        if item.assessment == assignment:
            rubrics.append(item)

    if request.method == "POST":
        totalMarks = 0
        actualMark = 0
        for i in range(len(rubrics)):
            item = rubrics[i]
            totalMarks += int(item.totalmarks)
            actualMark += int(request.form[item.criteria])


        # Now use student email and assessment to insert actual marks.
        if assignment == 'Assessment 1':
            student.assessment1 = (actualMark * 100 / totalMarks)
            db.session.commit()
            student.ass1feed = str(request.form['feed'])

        elif assignment == "Assessment 2":
            student.assessment2 = (actualMark * 100 / totalMarks)
            db.session.commit()
            student.ass2feed = str(request.form['feed'])
        elif assignment == 'Assignment 3':
            student.assessment3 = (actualMark  * 100 / totalMarks)
            db.session.commit()
            student.ass3feed = str(request.form['feed'])

        db.session.commit()
        return redirect(url_for('ViewStudents_Dem'))

    return render_template("markStudent.html", rubric = rubrics, markStudent = student, assessment=assignment, user = userrole )

@app.route("/genReport", methods=["GET", "POST"])
def genReport():

    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role

    if request.method == "POST":
        classes = request.form["selectClass"]
        Students = []
        AllStudents = FIT2101Student.query.all()
        for item in AllStudents:
            if item.classes == classes:
                Students.append(item)

        return render_template("reportPage.html", AllStudents = Students, user = userrole)
    
    if request.method == "GET":
        Student = FIT2101Student.query.all()
        classes = []
        for item in Student:
            if item.classes not in classes:
                classes.append(item.classes)

        return render_template("selectClass.html", data=classes, user = userrole)

@app.route("/addgroup", methods=["GET","POST"])
def addgroup():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role

    if request.method == 'POST':
       # If group name is empty redirect
       if request.form["groupname"] is None:
           return render_template("addGroups.html")

       email = request.form['s1_select']
       studentA = FIT2101Student.query.filter_by(email=email).first()
       studentA.groups = request.form["groupname"]

       email = request.form['s2_select']
       studentB = FIT2101Student.query.filter_by(email=email).first()
       studentB.groups = request.form["groupname"]

       email = request.form['s3_select']
       studentC = FIT2101Student.query.filter_by(email=email).first()
       studentC.groups = request.form["groupname"]
       db.session.commit()
       if userrole == "D":
           return redirect(url_for('dem_page'))
       else:
           return redirect(url_for('Lec_pageV2'))

    email = session['email']
    user = User.query.filter_by(email=email).first()
    userrole = user.role

    # Displaying Students:
    if user.role == 'D':
        stu_classes = user.classes
        listOfStudents = []
        students_list = FIT2101Student.query.all()
        for i in students_list:
            if i.classes == stu_classes:
                listOfStudents.append(i)

    elif user.role == 'L':
        listOfStudents = FIT2101Student.query.all()
        stu_classes = 'Lecturer'

    return render_template("addGroups.html", data=listOfStudents, user = userrole )


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
