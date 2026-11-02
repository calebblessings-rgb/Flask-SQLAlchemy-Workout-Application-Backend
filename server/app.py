
from flask import Flask, jsonify
from flask_migrate import Migrate

from server.models import db, Workout
from server.schemas import WorkoutSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

# Initialize the workout schema.
workout_schema = WorkoutSchema(many=True)


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify(workout_schema.dump(workouts)), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
