"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db
from sqlalchemy import func, orm


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/login")
def user_login():
    """Allow user to login"""

    #flash user "you are now signed up" OR "you are now logged in"
    return render_template("login.html")

@app.route("/handle-login", methods=['POST'])
def handle_login():
    """Action for login form; log a user in."""

    email = request.form['email']
    password = request.form['password']

    user = User(email=email, password=password) #To be used for adding new users

    try: 
        email_user = User.query.filter_by(email=email).one()
        # password_user = User.query.filter_by(password=password).one()
        # print password_user    
    except orm.exc.NoResultFound:
        email_user = None 
        print "Not in db"

    if email_user != None: 
        print "CODE REACHED IF STATEMENT"
        if password in email_user.password:
            # session['current_user'] = email
            flash("Logged in as %s" % email)
            return redirect("/")
        else:
            flash("Wrong password!")
            return redirect("/login")

    else:
        print "CODE REACHED ELSE STATEMENT"
        db.session.add(user)
        db.session.commit()
        print "USER ADDED TO DB"

    return render_template("login.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)


    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
