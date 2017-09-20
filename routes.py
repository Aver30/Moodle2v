from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import LoginForm, SignupForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zmbecnmseaboot:dd4459daa1a19c28aa3b6cbf3f9574bba805cd67f08fda71a30647e71b798f1a@ec2-54-235-102-25.compute-1.amazonaws.com:5432/ddqe9v9b3kauuf'
db.init_app(app)

app.secret_key = "development-key"



usersLec = {'email': "aakash@gmail.com", 'pwd': '1234'}

usersDem = {'email': "nn@gmail.com", 'pwd': '1234'}


# Add a log in
# newuser = User('Aakash', 'Verma', 'aakash@live.com', '12345')
# db.session.add(newuser)
# db.session.commit()

# Add Login details inside 
#newuser = User('Aakash', 'Verma' ,'adt@gmail.com', 'L', '1234')
#db.session.add(newuser)
#db.session.commit()


@app.route("/")
def index():
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

            # FOR HELP: https://stackoverflow.com/questions/23744171/flask-get-all-products-from-table-and-iterate-over-them
            # theList = User.query.all()

            if user is not None and user.password == password and user.role == 'L':     # If the user is lecturer
                return redirect(url_for('Lec_pageV2'))

            elif user is not None and user.password == password and user.role == 'D':   # If the user is demonstrator
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
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, 'D',form.password.data)
            db.session.add(newuser)
            db.session.commit()

            return redirect(url_for('Lec_pageV2'))

    elif request.method == "GET":
        return render_template('signup.html', form=form)



@app.route("/dem-page", methods=["GET", "POST"])
def dem_page():
    return render_template("dem-page.html")


@app.route("/demonstrator-after", methods=["GET", "POST"])
def demonstrator_after():
    return render_template("demonstrator-after.html")


@app.route("/Lec-pageV2", methods=["GET", "POST"])
def Lec_pageV2():
    return render_template("Lec-pageV2.html")


if __name__ == "__main__":
    app.run(debug=True)
