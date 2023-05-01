from flask import url_for
from flask_login import current_user
from app import models as m, db
from app import schema as s


def create_breadcrumbs(
    book_id: int,
    collection_path: tuple[int],
    section_id: int = 0,
    interpretation_id: int = 0,
) -> list[s.BreadCrumb]:
    crumples: list[s.BreadCrumb] = []
    book: m.Book = db.session.get(m.Book, book_id)
    if current_user.is_authenticated and book.user_id == current_user.id:
        # My Book
        crumples += [
            s.BreadCrumb(
                type=s.BreadCrumbType.MyBookList,
                url=url_for("book.my_books"),
                label="My Books",
            )
        ]
    else:
        # Not mine book
        crumples += [
            s.BreadCrumb(
                type=s.BreadCrumbType.AuthorBookList,
                url="#",
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

    for collection_id in collection_path:
        collection: m.Collection = db.session.get(m.Collection, collection_id)
        crumples += [
            s.BreadCrumb(
                type=s.BreadCrumbType.Collection,
                url=url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                ),
                label=collection.label,
            )
        ]
    if section_id != 0 and collection_path:
        section: m.Section = db.session.get(m.Section, section_id)
        if len(collection_path) == 2:
            crumples += [
                s.BreadCrumb(
                    type=s.BreadCrumbType.Section,
                    url=url_for(
                        "book.section_view",
                        book_id=book_id,
                        collection_id=collection_path[0],
                        sub_collection_id=collection_path[-1],
                    ),
                    label=section.label,
                )
            ]
        else:
            crumples += [
                s.BreadCrumb(
                    type=s.BreadCrumbType.Section,
                    url=url_for(
                        "book.section_view",
                        book_id=book_id,
                        collection_id=collection_path[0],
                        sub_collection_id=collection_path[0],
                    ),
                    label=section.label,
                )
            ]
        if interpretation_id != 0:
            interpretation: m.Interpretation = db.session.get(
                m.Interpretation, interpretation_id
            )
            if len(collection_path) == 2:
                crumples += [
                    s.BreadCrumb(
                        type=s.BreadCrumbType.Interpretation,
                        url=url_for(
                            "book.interpretation_view",
                            book_id=book_id,
                            collection_id=collection_path[0],
                            sub_collection_id=collection_path[-1],
                            section_id=section_id,
                        ),
                        label=interpretation.label,
                    )
                ]
            else:
                crumples += [
                    s.BreadCrumb(
                        type=s.BreadCrumbType.Interpretation,
                        url=url_for(
                            "book.interpretation_view",
                            book_id=book_id,
                            collection_id=collection_path[0],
                            sub_collection_id=collection_path[0],
                            section_id=section_id,
                        ),
                        label=interpretation.label,
                    )
                ]

    return crumples
