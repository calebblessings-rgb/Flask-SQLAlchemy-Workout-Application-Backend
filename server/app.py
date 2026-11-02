import os
from flask import Flask, jsonify, request
from marshmallow import ValidationError
from flask_migrate import Migrate

from server.models import db, Workout, Exercise, WorkoutExercises
from server.schemas import (
    WorkoutSchema,
    ExerciseSchema,
    WorkoutExercisesSchema
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///app.db"
)
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

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    # Check whether the exercise is associated with any workout.
    if exercise.workout_exercises:
        return jsonify({
            "error": "Cannot delete exercise because it is associated with a workout"
        }), 409

    try:
        db.session.delete(exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise deleted successfully"
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to delete exercise"
        }), 500

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):

    # Check whether the workout exists.
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    # Check whether the exercise exists.
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    # Prevent duplicate exercise associations.
    existing_association = WorkoutExercises.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if existing_association:
        return jsonify({
            "error": "Exercise is already associated with this workout"
        }), 409

    try:
        # Get optional workout exercise details.
        request_data = request.get_json() or {}

        # Add IDs from the URL to the request data.
        request_data["workout_id"] = workout_id
        request_data["exercise_id"] = exercise_id

        # Validate incoming data.
        association_data = WorkoutExercisesSchema().load(request_data)

        # Create the association.
        new_association = WorkoutExercises(**association_data)

        db.session.add(new_association)
        db.session.commit()

        return jsonify(
            WorkoutExercisesSchema().dump(new_association)
        ), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to add exercise to workout"
        }), 500

if __name__ == "__main__":
    app.run(port=5555, debug=True)
