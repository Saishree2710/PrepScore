from flask import Flask 
from extensions import db
from config import Config
from models import User, Topic, Subtopic, PracticeLog
from flask import render_template, request,session, redirect, url_for
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = "prepscore_secret_key"

db.init_app(app)

@app.route("/")
def home():
    return "PrepScore is running"
@app.route("/users")
def users():

    users = User.query.all()

    result = []

    for user in users:
        result.append(
            f"{user.user_id} - {user.name} - {user.email}"
        )

    return "<br>".join(result)
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        new_user=User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:

            if check_password_hash(user.password_hash, password):
               session["user_id"] = user.user_id
               session["user_name"] = user.name

               return redirect(url_for("dashboard"))
            else:
                return "Incorrect Password"

        else:
            return "User Not Found"

    return render_template("login.html")
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        user_name=session["user_name"]
    )
@app.route("/log-practice", methods=["GET", "POST"])
@login_required
def log_practice():

    topics = Topic.query.all()
    subtopics = Subtopic.query.all()

    if request.method == "POST":

        subtopic_id = int(request.form.get("subtopic"))
        questions_solved = int(request.form.get("questions_solved"))

        new_log = PracticeLog(
            user_id=session["user_id"],
            subtopic_id=subtopic_id,
            questions_solved=questions_solved
        )

        db.session.add(new_log)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template(
        "log_practice.html",
        topics=topics,
        subtopics=subtopics
    )
@app.route("/get-subtopics/<int:topic_id>")
def get_subtopics(topic_id):

    subtopics = Subtopic.query.filter_by(
        topic_id=topic_id
    ).all()

    result = []

    for subtopic in subtopics:
        result.append({
            "id": subtopic.subtopic_id,
            "name": subtopic.subtopic_name
        })

    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)