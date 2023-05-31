from app import models as m

BOOK = {
    "model": m.Book,
    "entity_id_field": "book_id",
}

COLLECTION = {
    "model": m.Collection,
    "entity_id_field": "collection_id",
}

SECTION = {
    "model": m.Section,
    "entity_id_field": "section_id",
}

INTERPRETATION = {
    "model": m.Interpretation,
    "entity_id_field": "interpretation_id",
}
