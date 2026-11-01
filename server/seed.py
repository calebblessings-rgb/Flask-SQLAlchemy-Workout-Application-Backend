from datetime import date
from server.app import app, db
from server.models import Exercise, Workout, WorkoutExercises


def seed_data():
    with app.app_context():
        # Clear existing records to prevent duplicates when reseeding.
        WorkoutExercises.query.delete()
        Workout.query.delete()
        Exercise.query.delete()

        # Create sample exercises.
        exercises = [
            Exercise(
                name="Push-ups",
                category="Strength",
                equipment_needed=False
            ),
            Exercise(
                name="Squats",
                category="Strength",
                equipment_needed=False
            ),
            Exercise(
                name="Running",
                category="Cardio",
                equipment_needed=False
            ),
            Exercise(
                name="Bench Press",
                category="Strength",
                equipment_needed=True
            )
        ]

        db.session.add_all(exercises)
        db.session.flush()

        # Create a sample workout.
        workout = Workout(
            date=date(2026, 11, 2),
            duration_minutes=45,
            notes="Full body workout"
        )

        db.session.add(workout)
        db.session.flush()

        # Connect exercises to the workout.
        workout_exercises = [
            WorkoutExercises(
                workout_id=workout.id,
                exercise_id=exercises[0].id,
                reps=15,
                sets=3
            ),
            WorkoutExercises(
                workout_id=workout.id,
                exercise_id=exercises[1].id,
                reps=20,
                sets=3
            ),
            WorkoutExercises(
                workout_id=workout.id,
                exercise_id=exercises[2].id,
                duration_seconds=600
            ),
            WorkoutExercises(
                workout_id=workout.id,
                exercise_id=exercises[3].id,
                reps=10,
                sets=3
            )
        ]

        db.session.add_all(workout_exercises)
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Exercises created: {len(exercises)}")
        print("Workouts created: 1")
        print(f"Workout exercises created: {len(workout_exercises)}")


if __name__ == "__main__":
    seed_data()
