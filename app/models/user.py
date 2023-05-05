from uuid import uuid4

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import BaseModel
from app.logger import log
from app import schema as s


def gen_uniq_id() -> str:
    return str(uuid4())


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    username = db.Column(db.String(64), unique=True, default=gen_uniq_id)
    password_hash = db.Column(db.String(256), default="")
    is_activated = db.Column(db.Boolean, default=False)
    wallet_id = db.Column(db.String(64), nullable=True)
    avatar_img = db.Column(db.Text, nullable=True)
    # Relationships
    stars = db.relationship("Book", secondary="books_stars", back_populates="stars")
    books = db.relationship("Book")

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter(
            func.lower(cls.username) == func.lower(user_id),
        ).first()
        if not user:
            log(log.WARNING, "user:[%s] not found", user_id)

        if user is not None and check_password_hash(user.password, password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.username}>"

    @property
    def json(self):
        u = s.User.from_orm(self)
        return u.json()


class AnonymousUser(AnonymousUserMixin):
    pass
