from flask_login import current_user
from app import models as m, db


def create_breadcrumbs(
    book_id: int,
    collection_id: int = 0,
    sub_collection_id: int = 0,
    section_id: int = 0,
):
    book = db.session.get(m.Book, book_id)
    if book.owner.id == current_user.id:
        pass
    if collection_id != 0:
        collection = db.session.get(m.Collection, collection_id)
    if sub_collection_id != 0:
        sub_collection = db.session.get(m.Collection, sub_collection_id)
    if section_id != 0:
        section = db.session.get(m.Section, section_id)
    pass
