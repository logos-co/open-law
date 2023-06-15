from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import and_, or_, func, distinct

from app.controllers import (
    register_book_verify_route,
)
from app.controllers.tags import (
    set_book_tags,
)
from app.controllers.delete_nested_book_entities import (
    delete_nested_book_entities,
)
from app.controllers.create_access_groups import (
    create_editor_group,
    create_moderator_group,
)
from app.controllers.require_permission import require_permission
from app.controllers.sorting import sort_by
from app import models as m, db, forms as f
from app.logger import log
from .bp import bp


@bp.route("/my_library", methods=["GET"])
def my_library():
    if current_user.is_authenticated:
        log(log.INFO, "Create query for my_library page for books")
        sort = request.args.get("sort")

        books: m.Book = (
            db.session.query(
                m.Book,
                m.Book.created_at.label("created_at"),
                func.count(distinct(m.Interpretation.id)).label(
                    "interpretations_count"
                ),
                func.count(distinct(m.BookStar.id)).label("stars_count"),
            )
            .join(
                m.BookStar,
                and_(
                    m.BookStar.book_id == m.Book.id,
                    m.BookStar.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(
                m.BookVersion,
                and_(
                    m.BookVersion.book_id == m.Book.id,
                    m.BookVersion.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(
                m.Section,
                and_(
                    m.BookVersion.id == m.Section.version_id,
                    m.Section.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(
                m.Interpretation,
                and_(
                    m.Interpretation.section_id == m.Section.id,
                    m.Interpretation.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(m.BookContributor, m.BookContributor.book_id == m.Book.id, full=True)
            .filter(
                or_(
                    m.Book.user_id == current_user.id,
                    m.BookContributor.user_id == current_user.id,
                ),
                m.Book.is_deleted == False,  # noqa: E712
            )
            .group_by(m.Book.id)
        )

        pagination, books = sort_by(books, sort)

        log(log.INFO, "Returns data for front end")

        return render_template(
            "book/my_library.html",
            books=books,
            page=pagination,
        )
    log(log.INFO, "Returns data for front end is user is anonym")

    return render_template(
        "book/my_library.html",
        books=[],
    )


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.CreateBookForm()
    if form.validate_on_submit():
        book: m.Book = m.Book(
            label=form.label.data, about=form.about.data, user_id=current_user.id
        )
        log(log.INFO, "Form submitted. Book: [%s]", book)
        book.save()
        version = m.BookVersion(semver="Active", book_id=book.id, is_active=True).save()
        root_collection = m.Collection(
            label="Root Collection", version_id=version.id, is_root=True
        ).save()
        tags = form.tags.data or ""
        set_book_tags(book, tags)

        # access groups
        editor_access_group = create_editor_group(book_id=book.id)
        moderator_access_group = create_moderator_group(book_id=book.id)
        access_groups = [editor_access_group, moderator_access_group]

        for access_group in access_groups:
            m.BookAccessGroups(book_id=book.id, access_group_id=access_group.id).save()
            m.CollectionAccessGroups(
                collection_id=root_collection.id, access_group_id=access_group.id
            ).save()
        # -------------

        flash("Book added!", "success")
        return redirect(url_for("book.my_library"))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.my_library"))


@bp.route("/<int:book_id>/edit", methods=["POST"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.BOOK,
    access=[m.Permission.Access.U],
    entities=[m.Book],
)
@login_required
def edit(book_id: int):
    form = f.EditBookForm()
    if form.validate_on_submit():
        book: m.Book = db.session.get(m.Book, book_id)
        label = form.label.data
        about = form.about.data
        tags = form.tags.data or ""
        set_book_tags(book, tags)

        book.label = label
        book.about = about
        log(log.INFO, "Update Book: [%s]", book)
        book.save()
        flash("Success!", "success")
        return redirect(url_for("book.collection_view", book_id=book_id))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.settings", book_id=book_id))


@bp.route("/<int:book_id>/delete", methods=["POST"])
@require_permission(
    entity_type=m.Permission.Entity.BOOK,
    access=[m.Permission.Access.D],
    entities=[m.Book],
)
@login_required
def delete(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)

    if not book or book.is_deleted:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("Book not found!", "danger")
        return redirect(url_for("book.my_library"))

    book.is_deleted = True
    delete_nested_book_entities(book)
    log(log.INFO, "Book deleted: [%s]", book)
    book.save()
    flash("Success!", "success")
    return redirect(url_for("book.my_library"))


@bp.route("/<int:book_id>/statistics", methods=["GET"])
def statistic_view(book_id: int):
    book = db.session.get(m.Book, book_id)
    active_tab = request.args.get("active_tab")
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_library"))
    return render_template("book/stat.html", book=book, active_tab=active_tab)


@bp.route("/favorite_books", methods=["GET"])
def favorite_books():
    if current_user.is_authenticated:
        log(log.INFO, "Creating query for books")
        sort = request.args.get("sort")

        books = (
            db.session.query(
                m.Book,
                m.Book.created_at.label("created_at"),
                func.count(distinct(m.Interpretation.id)).label(
                    "interpretations_count"
                ),
                func.count(distinct(m.BookStar.id)).label("stars_count"),
            )
            .join(
                m.BookStar,
                and_(
                    m.BookStar.book_id == m.Book.id,
                    m.BookStar.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(
                m.BookVersion,
                and_(
                    m.BookVersion.book_id == m.Book.id,
                    m.BookVersion.is_deleted == False,  # noqa: E712
                ),
            )
            .join(
                m.Section,
                and_(
                    m.BookVersion.id == m.Section.version_id,
                    m.Section.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(
                m.Interpretation,
                and_(
                    m.Interpretation.section_id == m.Section.id,
                    m.Interpretation.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .filter(
                m.Book.id == m.BookStar.book_id,
                m.BookStar.user_id == current_user.id,
                m.Book.is_deleted == False,  # noqa: E712
            )
            .group_by(m.Book.id)
        )

        pagination, books = sort_by(books, sort)

        log(log.INFO, "Returns data for front end")

        return render_template(
            "book/favorite_books.html",
            books=books,
            page=pagination,
        )
    return render_template("book/favorite_books.html", books=[])


@bp.route("/my_contributions", methods=["GET"])
def my_contributions():
    if current_user.is_authenticated:
        log(log.INFO, "Creating query for interpretations")
        sort = request.args.get("sort")

        interpretations = (
            db.session.query(
                m.Interpretation,
                m.Interpretation.score.label("score"),
                m.Interpretation.created_at.label("created_at"),
                func.count(distinct(m.Comment.interpretation_id)).label(
                    "comments_count"
                ),
            )
            .join(
                m.Comment,
                and_(
                    m.Comment.interpretation_id == m.Interpretation.id,
                    m.Comment.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .join(
                m.InterpretationVote,
                and_(
                    m.InterpretationVote.interpretation_id == m.Interpretation.id,
                    m.Interpretation.is_deleted == False,  # noqa: E712
                ),
                full=True,
            )
            .filter(
                or_(
                    and_(
                        m.Comment.user_id == current_user.id,
                        m.Comment.is_deleted.is_(False),
                    ),
                    and_(
                        m.Interpretation.user_id == current_user.id,
                        m.Interpretation.is_deleted.is_(False),
                    ),
                    and_(
                        m.InterpretationVote.user_id == current_user.id,
                        m.InterpretationVote.interpretation_id == m.Interpretation.id,
                    ),
                ),
                m.Interpretation.is_deleted == False,  # noqa: E712
                m.Interpretation.copy_of == 0,
            )
            .group_by(m.Interpretation.id)
        )

        pagination, interpretations = sort_by(interpretations, sort)

        log(log.INFO, "Returns data for front end")

        return render_template(
            "book/my_contributions.html",
            interpretations=interpretations,
            page=pagination,
        )
    return render_template("book/my_contributions.html", interpretations=[])
