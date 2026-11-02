from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1)
    )
    category = fields.String(
        required=True,
        validate=validate.Length(min=1)
    )
    equipment_needed = fields.Boolean(required=True)


class WorkoutExercisesSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(
        allow_none=True,
        validate=validate.Range(min=1)
    )
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.String(allow_none=True)
    workout_exercises = fields.Nested(
        WorkoutExercisesSchema,
        many=True,
        dump_only=True
    )