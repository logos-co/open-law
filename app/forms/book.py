from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app import models as m, db
from app.logger import log


class BaseBookForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(6, 256)])


class CreateBookForm(BaseBookForm):
    submit = SubmitField("Add new book")


class EditBookForm(BaseBookForm):
    book_id = StringField("User ID", [DataRequired()])
    submit = SubmitField("Edit book")

    def validate_label(self, field):
        label = field.data
        book_id = self.book_id.data

        existing_book: m.Book = m.Book.query.filter_by(
            is_deleted=False,
            label=label,
        ).first()
        if existing_book:
            log(
                log.WARNING, "Book with label [%s] already exists: [%s]", label, book_id
            )
            raise ValidationError("Book label must be unique!")
