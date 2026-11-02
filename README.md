# Flask SQLAlchemy Workout Application Backend

## Project Description

The Flask SQLAlchemy Workout Application Backend is a RESTful API that manages exercises, workouts, and the exercises performed during each workout.

The application uses Flask to build the API, SQLAlchemy for database management, Marshmallow for serialization and validation, and SQLite as the default database.

## Features

- Create, retrieve, and delete workouts.
- Create, retrieve, and delete exercises.
- Add exercises to existing workouts.
- Record repetitions, sets, and duration for workout exercises.
- Retrieve workouts with their associated exercises.
- Retrieve exercises with their associated workouts.
- Validate incoming request data.
- Enforce database constraints and model-level validations.
- Manage database changes using Flask-Migrate.
- Run automated API tests using pytest.

## Technologies Used

- Python 3.11
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv
- pytest

## Project Structure

```text
Flask-SQLAlchemy-Workout-Application-Backend/
│
├── migrations/
│   └── versions/
│
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
│
├── tests/
│   └── test_api.py
│
├── .gitignore
├── .python-version
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Database Models

The application uses three main database models:

### 1. Exercise

Stores information about individual exercises.

Fields:
- `id`: Primary key.
- `name`: Exercise name.
- `category`: Exercise category.
- `equipment_needed`: Indicates whether equipment is required.

### 2. Workout

Stores information about workout sessions.

Fields:
- `id`: Primary key.
- `date`: Workout date.
- `duration_minutes`: Workout duration in minutes.
- `notes`: Additional workout notes.

### 3. WorkoutExercises

Connects workouts and exercises through an association model.

Fields:
- `id`: Primary key.
- `workout_id`: Foreign key referencing a workout.
- `exercise_id`: Foreign key referencing an exercise.
- `reps`: Number of repetitions.
- `sets`: Number of sets.
- `duration_seconds`: Exercise duration in seconds.

The association model allows an exercise to belong to multiple workouts and a workout to contain multiple exercises.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/calebblessings-rgb/Flask-SQLAlchemy-Workout-Application-Backend.git
```

### 2. Navigate into the project directory

```bash
cd Flask-SQLAlchemy-Workout-Application-Backend
```

### 3. Install dependencies

Install Pipenv if it is not already installed:

```bash
python3 -m pip install --user pipenv
```

Install the project dependencies:

```bash
pipenv install
```

### 4. Activate the virtual environment

```bash
pipenv shell
```

Alternatively, run commands using `pipenv run` without activating the environment.

## Database Setup

The application uses SQLite by default. Its database is configured to use `instance/app.db`.

The project already includes database migration files.

Apply the migrations using:

```bash
pipenv run flask --app server.app db upgrade
```

This creates the database tables using the existing migration history.

### Seed the database

Populate the database with sample exercises, workouts, and workout-exercise associations:

```bash
pipenv run python -m server.seed
```

The seed script provides sample records for testing the application.

**Note:** The seed script resets existing sample records before inserting its data. Use it with a development database.

## Running the Application

Start the Flask development server:

```bash
pipenv run flask --app server.app run --debug
```

The application will be available at:

```text
http://127.0.0.1:5000
```

You can use Postman, curl, or another API client to interact with the endpoints.

## API Endpoints

The application provides the following REST API endpoints.

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve a workout by ID |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve an exercise by ID |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example API Requests

### 1. Create a workout

**POST** `/workouts`

Request body:

```json
{
    "date": "2026-11-02",
    "duration_minutes": 45,
    "notes": "Full body workout"
}
```

### 2. Create an exercise

**POST** `/exercises`

Request body:

```json
{
    "name": "Push-ups",
    "category": "Strength",
    "equipment_needed": false
}
```

### 3. Add an exercise to a workout

**POST** `/workouts/1/exercises/1/workout_exercises`

Request body:

```json
{
    "reps": 15,
    "sets": 3,
    "duration_seconds": 60
}
```

The workout and exercise IDs in this example must exist in the database.

### 4. Retrieve all workouts

**GET** `/workouts`

### 5. Retrieve all exercises

**GET** `/exercises`

## Validation and Error Handling

The application uses validation at different levels:

- **Database constraints:** Enforce required fields and positive numeric values.
- **Model validations:** Validate values when model instances are created or updated.
- **Schema validations:** Validate incoming API request data using Marshmallow.

The API also handles errors such as:

- Missing workouts or exercises.
- Invalid request data.
- Duplicate exercise associations.
- Attempts to delete exercises that are already associated with workouts.

## Running Automated Tests

The project includes automated API tests covering workout operations, exercise operations, and workout-exercise associations.

Run the test suite using:

```bash
pipenv run python -m pytest -v
```

The current test suite contains 18 tests covering:

- Retrieving workouts.
- Creating workouts.
- Retrieving individual workouts.
- Deleting workouts.
- Retrieving exercises.
- Creating exercises.
- Retrieving individual exercises.
- Deleting exercises.
- Adding exercises to workouts.
- Preventing duplicate associations.
- Rejecting invalid association data.
- Handling missing records.
- Preventing deletion of associated exercises.

**Latest test result: 18 passed.**

## Author

Caleb Blessings

GitHub: [calebblessings-rgb](https://github.com/calebblessings-rgb)
