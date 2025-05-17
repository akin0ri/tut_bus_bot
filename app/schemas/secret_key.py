from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import SecretKey

class SecretKeySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SecretKey
        load_instance = True 