from datetime import datetime

from app import db


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
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
