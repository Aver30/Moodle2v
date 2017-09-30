from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, FIT2101Student
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

            print("THIS IS WORKING\n \n \n\n\n")
            return render_template('signup.html', form=form)
        else:
            
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, 'D', form.password.data, form.classes.data, 'fit2101');
            db.session.add(newuser)
            db.session.commit()
            print("THIS IS WORKING\n \n \n\n\n")
            return redirect(url_for('Lec_pageV2'))

    elif request.method == "GET":
        return render_template('signup.html', form=form)


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

    email = session['email']
    user = User.query.filter_by(email=email).first()
    nameDem = user.firstname
    return render_template("dem-page.html", name = nameDem)


@app.route("/Lec-pageV2", methods=["GET", "POST"])
def Lec_pageV2():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    nameDem = user.firstname + " " + user.lastname

    # If nothing in session, then return to index page
    if session['email'] is None:
        return redirect(url_for('index'))

    return render_template("Lec-pageV2.html", name = nameDem)

@app.route("/ViewStudents_Dem", methods=["GET", "POST"])
def ViewStudents_Dem():
    listOfStudents = FIT2101Student.query.all()
    return render_template("ViewStudents_Dem.html", students = listOfStudents)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
