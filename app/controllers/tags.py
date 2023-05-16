from app import models as m, db
from app.logger import log


def set_book_tags(book: m.Book, tags: str):
    book_tags = m.BookTags.query.filter_by(book_id=book.id).all()
    for book_tag in book_tags:
        db.session.delete(book_tag)

    tags_names = [tag.title() for tag in tags.split(",") if len(tag)]

    for tag_name in tags_names:
        if len(tag_name) > 32:
            log(
                log.ERROR,
                "Cannot create Tag [%s]. Exceeded name length. Current length: [%s]",
                tag_name,
                len(tag_name),
            )
            continue

        tag = m.Tag.query.filter_by(name=tag_name).first()
        if not tag:
            log(log.INFO, "Create Tag: [%s]", tag)
            tag = m.Tag(name=tag_name).save()

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
        if len(tag_name) > 32:
            log(
                log.ERROR,
                "Cannot create Tag [%s]. Exceeded name length. Current length: [%s]",
                tag_name,
                len(tag_name),
            )
            continue

        tag = m.Tag.query.filter_by(name=tag_name).first()
        if not tag:
            log(log.INFO, "Create Tag: [%s]", tag)
            tag = m.Tag(name=tag_name).save()

        comment_tag = m.CommentTags(tag_id=tag.id, comment_id=comment.id)
        log(log.INFO, "Create CommentTags: [%s]", comment_tag)
        comment_tag.save(False)
    db.session.commit()
