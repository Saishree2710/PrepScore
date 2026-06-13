from flask import Flask 
from extensions import db
from config import Config
from models import User, Topic, Subtopic, PracticeLog
from flask import render_template, request

app = Flask(__name__)
app.config.from_object(Config)

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
            password_hash=password
        )
        db.session.add(new_user)
        db.session.commit()
        return "User Created Successfully!"

    return render_template("register.html")
    

if __name__=="__main__":
    app.run(debug=True)