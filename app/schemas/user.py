from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True 