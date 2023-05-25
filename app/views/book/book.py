from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required, current_user
from sqlalchemy import and_, or_

from app.controllers import (
    create_pagination,
    register_book_verify_route,
)
from app.controllers.tags import (
    set_book_tags,
)
from app.controllers.delete_nested_book_entities import (
    delete_nested_book_entities,
)
from app import models as m, db, forms as f
from app.logger import log
from .bp import bp


@bp.route("/all", methods=["GET"])
def get_all():
    q = request.args.get("q", type=str, default=None)
    books: m.Book = m.Book.query.order_by(m.Book.id)
    if q:
        books = books.filter(m.Book.label.like(f"{q}"))

    pagination = create_pagination(total=books.count())

    return render_template(
        "book/all.html",
        books=books.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        search_query=q,
        all_books=True,
    )


@bp.route("/my_library", methods=["GET"])
def my_library():
    if current_user.is_authenticated:
        books: m.Book = m.Book.query.order_by(m.Book.id)
        books = books.filter_by(user_id=current_user.id, is_deleted=False)
        pagination = create_pagination(total=books.count())

        return render_template(
            "book/my_library.html",
            books=books.paginate(page=pagination.page, per_page=pagination.per_page),
            page=pagination,
        )
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
        version = m.BookVersion(semver="1.0.0", book_id=book.id).save()
        m.Collection(
            label="Root Collection", version_id=version.id, is_root=True
        ).save()
        tags = form.tags.data
        if tags:
            set_book_tags(book, tags)

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
@login_required
def edit(book_id: int):
    form = f.EditBookForm()
    if form.validate_on_submit():
        book: m.Book = db.session.get(m.Book, book_id)
        label = form.label.data
        about = form.about.data
        tags = form.tags.data
        if tags:
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
@login_required
def delete(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)

    if not book or book.is_deleted:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
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
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_library"))
    return render_template("book/stat.html", book=book)


@bp.route("/favorite_books", methods=["GET"])
def favorite_books():
    if current_user.is_authenticated:
        books = (
            db.session.query(
                m.Book,
            )
            .filter(
                and_(
                    m.Book.id == m.BookStar.book_id,
                    m.BookStar.user_id == current_user.id,
                    m.Book.is_deleted.is_(False),
                )
            )
            .order_by(m.Book.created_at.desc())
        )

        books = books.filter_by(is_deleted=False)
        pagination = create_pagination(total=books.count())

        return render_template(
            "book/favorite_books.html",
            books=books.paginate(page=pagination.page, per_page=pagination.per_page),
            page=pagination,
        )
    return render_template("book/favorite_books.html", books=[])


@bp.route("/my_contributions", methods=["GET"])
def my_contributions():
    if current_user.is_authenticated:
        interpretations = (
            db.session.query(
                m.Interpretation,
            )
            .filter(
                or_(
                    and_(
                        m.Interpretation.id == m.Comment.interpretation_id,
                        m.Comment.user_id == current_user.id,
                        m.Comment.is_deleted.is_(False),
                        m.Interpretation.is_deleted.is_(False),
                    ),
                    and_(
                        m.Interpretation.user_id == current_user.id,
                        m.Interpretation.is_deleted.is_(False),
                    ),
                )
            )
            .group_by(m.Interpretation.id)
            .order_by(m.Interpretation.created_at.desc())
        )

        pagination = create_pagination(total=interpretations.count())

        return render_template(
            "book/my_contributions.html",
            interpretations=interpretations.paginate(
                page=pagination.page, per_page=pagination.per_page
            ),
            page=pagination,
        )
    return render_template("book/my_contributions.html", interpretations=[])
