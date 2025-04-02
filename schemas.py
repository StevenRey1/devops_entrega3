from marshmallow import Schema, fields, ValidationError
import uuid
class BlacklistSchema(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.UUID(required=True)
    blocked_reason = fields.String(max_length=255, allow_none=True)

    #def validate_uuid(uuid_string):
    #    try:
    #        uuid.UUID(uuid_string)
    #    except ValueError:
    #        raise ValidationError("Not a valid UUID")