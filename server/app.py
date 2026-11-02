from flask import Flask, jsonify, request
from marshmallow import ValidationError
from flask_migrate import Migrate

from server.models import db, Workout, Exercise
from server.schemas import WorkoutSchema, ExerciseSchema

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

# Initialize the exercise schema.
exercise_schema = ExerciseSchema(many=True)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(exercise_schema.dump(exercises)), 200

@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(ExerciseSchema().dump(exercise)), 200

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(WorkoutSchema().dump(workout)), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        # Validate and deserialize incoming JSON.
        workout_data = WorkoutSchema().load(request.get_json())

        # Create a new Workout object.
        new_workout = Workout(**workout_data)

        # Save the workout to the database.
        db.session.add(new_workout)
        db.session.commit()

        # Return the newly created workout.
        return jsonify(WorkoutSchema().dump(new_workout)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to create workout"}), 500

@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        # Validate and deserialize incoming JSON.
        exercise_data = ExerciseSchema().load(request.get_json())

        # Create a new Exercise object.
        new_exercise = Exercise(**exercise_data)

        # Save the exercise to the database.
        db.session.add(new_exercise)
        db.session.commit()

        # Return the newly created exercise.
        return jsonify(ExerciseSchema().dump(new_exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Unable to create exercise"}), 500

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    try:
        db.session.delete(workout)
        db.session.commit()

        return jsonify({
            "message": "Workout deleted successfully"
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to delete workout"
        }), 500

if __name__ == "__main__":
    app.run(port=5555, debug=True)
