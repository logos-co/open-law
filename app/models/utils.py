from datetime import datetime

from flask_login import current_user

from app import db


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
        if hasattr(self, "updated_at"):
            self.updated_at = datetime.now()
            self.updated_by = current_user.id

        db.session.add(self)
        if commit:
            db.session.commit()
        return self


class BaseModel(db.Model, ModelMixin):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)


# Add your own utility classes and functions here.
