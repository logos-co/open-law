from flask import url_for
from flask_login import current_user

from app import models as m, db

from app.logger import log


def create_notification(
    entity: m.Notification.Entities,
    action: m.Notification.Actions,
    entity_id: int,
    user_id: int,
    text: str,
    link: str,
):
    m.Notification(
        link=link,
        text=text,
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
    ).save()
    log(
        log.INFO,
        "Create notification for user with id [%s]",
        user_id,
    )


def section_notification(action: m.Notification.Actions, entity_id: int, user_id: int):
    text = None
    link = None
    section: m.Section = db.session.get(m.Section, entity_id)
    book: m.Book = db.session.get(m.Book, section.book_id)
    match action:
        case m.Notification.Actions.CREATE:
            text = f"{current_user.username} create a new section on {book.label}"
            link = (
                url_for("book.collection_view", book_id=book.id)
                + f"#section-{section.label}"
            )

        case m.Notification.Actions.EDIT:
            text = f"{current_user.username} renamed a section on {book.label}"
            link = (
                url_for("book.collection_view", book_id=book.id)
                + f"#section-{section.label}"
            )

        case m.Notification.Actions.DELETE:
            text = f"{current_user.username} delete a section on {book.label}"
            link = url_for("book.collection_view", book_id=book.id)

    create_notification(
        m.Notification.Entities.SECTION, action, entity_id, user_id, text, link
    )


def collection_notification(
    action: m.Notification.Actions, entity_id: int, user_id: int
):
    text = None
    link = None
    collection: m.Collection = db.session.get(m.Collection, entity_id)
    book: m.Book = db.session.get(m.Book, collection.book_id)
    match action:
        case m.Notification.Actions.CREATE:
            text = f"{current_user.username} create a new collection on {book.label}"
            link = (
                url_for("book.collection_view", book_id=book.id)
                + f"#collection-{collection.label}"
            )

        case m.Notification.Actions.EDIT:
            text = f"{current_user.username} renamed a collection on {book.label}"
            link = (
                url_for("book.collection_view", book_id=book.id)
                + f"#collection-{collection.label}"
            )

        case m.Notification.Actions.DELETE:
            text = f"{current_user.username} delete a collection on {book.label}"
            link = url_for("book.collection_view", book_id=book.id)
    create_notification(
        m.Notification.Entities.COLLECTION, action, entity_id, user_id, text, link
    )


def interpretation_notification(
    action: m.Notification.Actions, entity_id: int, user_id: int
):
    text = None
    link = None
    interpretation: m.Interpretation = db.session.get(m.Interpretation, entity_id)
    section: m.Section = db.session.get(m.Section, interpretation.section_id)
    book: m.Book = db.session.get(m.Book, interpretation.book.id)
    match action:
        case m.Notification.Actions.CREATE:
            text = f"New interpretation to {section.label} on {book.label}"
            link = url_for(
                "book.interpretation_view",
                book_id=book.id,
                section_id=section.id,
            )

        case m.Notification.Actions.DELETE:
            text = "A moderator has removed your interpretation"
            link = url_for(
                "book.interpretation_view",
                book_id=book.id,
                section_id=section.id,
            )

        case m.Notification.Actions.APPROVE:
            if user_id == book.owner.id:
                if current_user.id == book.owner.id:
                    return
                # This for the book owner
                text = f"{current_user.username} approved an interpretation for {section.label} on {book.label}"
                link = url_for(
                    "book.interpretation_view",
                    book_id=book.id,
                    section_id=section.id,
                )
            elif user_id == interpretation.user_id and user_id != book.owner.id:
                # This for the interpretation owner
                text = f"Your interpretation has been approved for {section.label} on {book.label}"
                link = url_for(
                    "book.interpretation_view",
                    book_id=book.id,
                    section_id=section.id,
                )
            else:
                return

    create_notification(
        m.Notification.Entities.INTERPRETATION, action, entity_id, user_id, text, link
    )


def comment_notification(action: m.Notification.Actions, entity_id: int, user_id: int):
    text = None
    link = None
    comment: m.Comment = db.session.get(m.Comment, entity_id)
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, comment.interpretation_id
    )
    section: m.Section = db.session.get(m.Section, interpretation.section_id)
    book: m.Book = db.session.get(m.Book, comment.book.id)
    match action:
        case m.Notification.Actions.CREATE:
            text = "New comment to your interpretation"
            link = url_for(
                "book.qa_view",
                book_id=book.id,
                interpretation_id=comment.interpretation_id,
            )

        case m.Notification.Actions.DELETE:
            text = "A moderator has removed your comment"
            link = url_for(
                "book.qa_view",
                book_id=book.id,
                interpretation_id=comment.interpretation_id,
            )

        case m.Notification.Actions.APPROVE:
            if user_id == comment.user_id and user_id != book.owner.id:
                text = f"Your comment has been approved for {section.label} on {book.label}"
                link = url_for(
                    "book.qa_view",
                    book_id=comment.book.id,
                    interpretation_id=comment.interpretation_id,
                )
            elif user_id == book.owner.id:
                text = f"{current_user.username} approved an comment for {section.label} on {book.label}"
                link = url_for(
                    "book.qa_view",
                    book_id=comment.book.id,
                    interpretation_id=comment.interpretation_id,
                )
            else:
                return

        case m.Notification.Actions.MENTION:
            text = "You been mention in comment"
            link = url_for(
                "book.qa_view",
                book_id=book.id,
                interpretation_id=comment.interpretation_id,
            )

    create_notification(
        m.Notification.Entities.COMMENT, action, entity_id, user_id, text, link
    )


def contributor_notification(
    action: m.Notification.Actions, entity_id: int, user_id: int
):
    text = None
    link = None
    book: m.Book = db.session.get(m.Book, entity_id)
    match action:
        case m.Notification.Actions.CONTRIBUTING:
            text = f"You've been added to {book.label} as an Editor/Moderator"
            link = url_for(
                "book.collection_view",
                book_id=book.id,
            )

        case m.Notification.Actions.DELETE:
            text = f"You've been removed from {book.label} as an Editor/Moderator"
            link = url_for(
                "book.collection_view",
                book_id=book.id,
            )

    create_notification(
        m.Notification.Entities.BOOK, action, entity_id, user_id, text, link
    )
