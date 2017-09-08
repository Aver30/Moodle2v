from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/moodle2v'
db.init_app(app)

app.secret_key = "development-key"


usersLec = {'email': "aakash@gmail.com", 'pwd': '1234'}

usersDem = {'email': "nn@gmail.com", 'pwd': '1234'}


# Add a log in
# newuser = User('Aakash', 'Verma', 'aakash@live.com', '12345')
# db.session.add(newuser)
# db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logLec", methods=["GET","POST"])
def logLec():
    form = LoginForm()
    if request.method == "POST":
        if form.validate() == False:
            return render_template("logLec.html", form=form)
        else:
            email = form.email.data
            password = form.password.data
                    
            # Check if user in system
            if usersLec['email'] == email and usersLec['pwd'] == password:
                return redirect(url_for('lec_page'))
            else:
                return redirect(url_for('logLec'))
    elif request.method == 'GET':
        return render_template('logLec.html', form=form)



@app.route("/logDem", methods=["GET","POST"])
def logDem():
    form = LoginForm()
        
    if request.method == "POST":
        if form.validate() == False:
            return render_template("logDem.html", form=form)
        else:
            email = form.email.data
            password = form.password.data
                    
            # Check if user in system
            if usersDem['email'] == email and usersDem['pwd'] == password:
                return redirect(url_for('dem_page'))
            else:
                return redirect(url_for('logLec'))
            
    elif request.method == 'GET':
        return render_template('logDem.html', form=form)



@app.route("/dem-page", methods=["GET", "POST"])
def dem_page():
    return render_template("dem-page.html")



@app.route("/demonstrator-after", methods=["GET", "POST"])
def demonstrator_after():
    return render_template("demonstrator-after.html")


@app.route("/lec-page", methods=["GET", "POST"])
def lec_page():
    return render_template("lec-page.html")


if __name__ == "__main__":
    app.run(debug=True)
