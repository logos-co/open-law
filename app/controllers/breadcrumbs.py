from flask import url_for
from flask_login import current_user

from app import models as m, db
from app import schema as s


def create_collections_breadcrumb(
    bread_crumbs: list[s.BreadCrumb], collection: m.Collection
) -> list[s.BreadCrumb]:
    bread_crumbs += [
        s.BreadCrumb(
            type=s.BreadCrumbType.Collection,
            url="",
            label=collection.label,
        )
    ]

    if collection.parent and not collection.parent.is_root:
        create_collections_breadcrumb(bread_crumbs, collection.parent)


def create_breadcrumbs(
    book_id: int,
    collection_path: tuple[int],
    section_id: int = 0,
    interpretation_id: int = 0,
    collection_id: int = 0,
) -> list[s.BreadCrumb]:
    """
    How breadcrumbs look like:

    Book List -> Book Name -> Top Level Collection -> SubCollection -> Section -> Interpretation

    - If i am not owner of a book
    John's books -> Book Name -> Top Level Collection -> SubCollection -> Section -> Interpretation

    - If i am owner
    My Books -> Book Title -> Part I -> Chapter X -> Paragraph 1.7 -> By John
    """

    crumples: list[s.BreadCrumb] = []
    book: m.Book = db.session.get(m.Book, book_id)
    if current_user.is_authenticated and book.user_id == current_user.id:
        # My Book
        crumples += [
            s.BreadCrumb(
                type=s.BreadCrumbType.MyBookList,
                url=url_for("book.my_library"),
                label="My Books",
            )
        ]
    else:
        # Not mine book
        crumples += [
            s.BreadCrumb(
                type=s.BreadCrumbType.AuthorBookList,
                url="",
                label=book.owner.username + "'s books",
            )
        ]

    crumples += [
        s.BreadCrumb(
            type=s.BreadCrumbType.Collection,
            url=url_for("book.collection_view", book_id=book_id),
            label=book.label,
        )
    ]

    collections_crumbs = []
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    create_collections_breadcrumb(collections_crumbs, collection)
    crumples += collections_crumbs.reverse()

    if section_id and collection_id:
        section: m.Section = db.session.get(m.Section, section_id)
        crumples += [
            s.BreadCrumb(
                type=s.BreadCrumbType.Section,
                url=url_for(
                    "book.interpretation_view",
                    book_id=book_id,
                    section_id=section_id,
                ),
                label=section.label,
            )
        ]
    return crumples
