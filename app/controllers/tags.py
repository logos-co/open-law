from app import models as m, db
from app.logger import log


def get_or_create_tag(tag_name: str):
    if len(tag_name) > 32:
        log(
            log.ERROR,
            "Cannot create Tag [%s]. Exceeded name length. Current length: [%s]",
            tag_name,
            len(tag_name),
        )
        raise ValueError("Exceeded name length")

    tag = m.Tag.query.filter_by(name=tag_name).first()
    if not tag:
        log(log.INFO, "Create Tag: [%s]", tag)
        tag = m.Tag(name=tag_name).save()

    return tag


def set_book_tags(book: m.Book, tags: str):
    book_tags = m.BookTags.query.filter_by(book_id=book.id).all()
    for book_tag in book_tags:
        db.session.delete(book_tag)

    tags_names = [tag.title() for tag in tags.split(",") if len(tag)]

    for tag_name in tags_names:
        try:
            tag = get_or_create_tag(tag_name)
        except ValueError as e:
            if str(e) == "Exceeded name length":
                continue
            log(
                log.CRITICAL,
                "Unexpected error [%s]",
                str(e),
            )
            raise e

        book_tag = m.BookTags(tag_id=tag.id, book_id=book.id)
        log(log.INFO, "Create BookTag: [%s]", book_tag)
        book_tag.save(False)
    db.session.commit()


def set_comment_tags(comment: m.Comment, tags: str):
    comment_tags = m.CommentTags.query.filter_by(comment_id=comment.id).all()
    for tag in comment_tags:
        db.session.delete(tag)
    tags_names = [tag.title() for tag in tags.split(",") if len(tag)]

    for tag_name in tags_names:
        try:
            tag = get_or_create_tag(tag_name)
        except ValueError as e:
            if str(e) == "Exceeded name length":
                continue
            log(
                log.CRITICAL,
                "Unexpected error [%s]",
                str(e),
            )
            raise e

        comment_tag = m.CommentTags(tag_id=tag.id, comment_id=comment.id)
        log(log.INFO, "Create CommentTags: [%s]", comment_tag)
        comment_tag.save(False)
    db.session.commit()


def set_interpretation_tags(interpretation: m.InterpretationTag, tags: str):
    interpretation_tags = m.InterpretationTag.query.filter_by(
        interpretation_id=interpretation.id
    ).all()
    for tag in interpretation_tags:
        db.session.delete(tag)
    tags_names = [tag.title() for tag in tags.split(",") if len(tag)]

    for tag_name in tags_names:
        try:
            tag = get_or_create_tag(tag_name)
        except ValueError as e:
            if str(e) == "Exceeded name length":
                continue
            log(
                log.CRITICAL,
                "Unexpected error [%s]",
                str(e),
            )
            raise e

        interpretation_tag = m.InterpretationTag(
            tag_id=tag.id, interpretation_id=interpretation.id
        )
        log(log.INFO, "Create InterpretationTag: [%s]", interpretation_tag)
        interpretation_tag.save(False)
    db.session.commit()
