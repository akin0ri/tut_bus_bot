from marshmallow import Schema, fields

class TimetableSchema(Schema):
    id = fields.Int(dump_only=True)
    route = fields.Str(required=True)
    direction = fields.Int(required=True)
    departure_time = fields.Time(required=True)
    arrival_time = fields.Time(allow_none=True)
    is_shuttle = fields.Bool()
    shuttle_start = fields.Time(allow_none=True)
    shuttle_end = fields.Time(allow_none=True)
    valid_from = fields.Date(required=True)
    valid_to = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 