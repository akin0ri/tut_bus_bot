from marshmallow import Schema, fields

class ExtraTimetableSchema(Schema):
    id = fields.Int(dump_only=True)
    timetable_id = fields.Int(required=True)
    special_date = fields.Date(required=True)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    used_at = fields.DateTime(allow_none=True) 