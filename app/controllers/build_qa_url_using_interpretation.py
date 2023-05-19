from flask import url_for

from app import models as m


def build_qa_url_using_interpretation(interpretation: m.Interpretation):
    section: m.Section = interpretation.section
    collection: m.Collection = section.collection
    sub_collection = None
    if collection.is_leaf and collection.parent.is_root:
        collection: m.Collection = collection.parent
        sub_collection: m.Collection = collection
    book: m.Book = section.version.book

    url = url_for(
        "book.qa_view",
        book_id=book.id,
        collection_id=collection.id,
        sub_collection_id=sub_collection.id if sub_collection else None,
        section_id=section.id,
        interpretation_id=interpretation.id,
    )
    return url
