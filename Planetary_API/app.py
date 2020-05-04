from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__) #__name__ means it will take the name from the name of this current script
basedir = os.path.abspath(os.path.dirname(__file__)) # This finds the directory name with this current file and then it finds the absolute directory of it from the machine and stores it
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "planets.db")

db = SQLAlchemy(app)
ma = Marshmallow(app)

#################################################################################### DB CLI COMMANDS ####################################################################################
@app.cli.command("create_db") # This is a command line argument that triggers an action
def create_db():
    db.create_all()
    print("Database Created!")

@app.cli.command("drop_db")
def drop_db():
    db.drop_all()
    print("Database Dropped!")

@app.cli.command("seed_db")
def seed_db():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=2.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                         planet_type='Class K',
                         home_star='Sol',
                         mass=4.867e24,
                         radius=3760,
                         distance=67.24e6)

    earth = Planet(planet_name='Earth',
                     planet_type='Class M',
                     home_star='Sol',
                     mass=5.972e24,
                     radius=3959,
                     distance=92.96e6)

    db.session.add(mercury) # Adds entries to their tables
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William',
                     last_name='Herschel',
                     email='test@test.com',
                     password='P@ssw0rd')

    db.session.add(test_user)
    db.session.commit() # Saves the added
    print('Database seeded!')

#################################################################################### DB Classes/ Tables ####################################################################################
class User(db.Model):
    __tablename__ = "users" # This controls the name of the table
    id = Column(Integer, primary_key=True) # These are the instance variables that are created/ treated as columns in an actual table
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    username = Column(String, unique=True)


class Planet(db.Model):
    __tablename__ = "planets"
    planet_id = Column(Integer, primary_key = True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    radius = Column(Float)
    mass = Column(Float)
    distance = Column(Float)


#################################################################################### Serialization Classes ####################################################################################
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password", "username") # This showcases the format that the data will be returned in

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ("planet_id", "planet_name", "planet_type", "home_star", "radius", "mass", "distance")

user_schema = UserSchema() # This is a schema that is capable of serializing only 1 object
users_schema = UserSchema(many=True) # This is a duplicate schema that will be capable of serializing multiple objects

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

#################################################################################### Routes ####################################################################################

@app.route("/") # These are decorators in flask and endpoints in API talk
def home():
    return "Home"


@app.route("/home") 
def new_home():
    return "This is the new home page."


@app.route("/jsonify")
def json_message():
    return jsonify(message="This is a JSON message.")


@app.route("/parameters") # Decorators cannot have the same name as the actual function they call
def parameter():
    name = request.args.get("name") # This retrieves particular arguments from the Request URL
    age = int(request.args.get("age"))

    if age < 18:
        return jsonify(message=name+" is not old enough for access"), 401
    else:
        return jsonify(message="Message")


@app.route("/url/<string:param1>/<int:param2>") # Flask can also set URLs to have particular structures so it can properly extract info. You can also specify the datatype of the parameters
def parameter_matching(param1: str, param2: int):
    if param2 == 18:
        return jsonify(message="You got lucky " + param1 + ", you just turned 18")
    elif param2 < 18:
        return jsonify(message="Begone heathen! You are not old enough")
    else:
        return jsonify(message="Drinks on me")


@app.route("/planets", methods=["GET"])
def get_planet():
    planets_list = Planet.query.all() # This function will query the table created by the Planet Class
    call_result =  planets_schema.dump(planets_list) # You need to serialize the data in order to turn it into a JSON format. Serialization is a process that turns tables into JSON
    return jsonify(call_result.data)

@app.route("/register", methods=["POST"])
def register_user():
    email = request.form["email"]
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify(message="This email is already taken"), 409 # Conflict
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify("New User successfully registered"), 201 # 201 = new record


if __name__ == "__main__":
    app.run(debug=True)