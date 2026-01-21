# server/app.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Earthquake

# -----------------------
# Flask App Configuration
# -----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# -----------------------
# Routes
# -----------------------

# Get earthquake by id


@app.route("/earthquakes/<int:id>")
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake:
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

# Get earthquakes with minimum magnitude


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_data = [
        {
            "id": q.id,
            "location": q.location,
            "magnitude": q.magnitude,
            "year": q.year
        } for q in quakes
    ]
    return jsonify({
        "count": len(quakes_data),
        "quakes": quakes_data
    }), 200


# -----------------------
# Run server (optional)
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, port=5555)
