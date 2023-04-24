from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required

from app import db, models as m, forms as f
from app.logger import log
from app.controllers import create_pagination

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route("/", methods=["GET"])
def get_all():
    q = request.args.get("q", type=str, default=None)
    books = m.Book.query.order_by(m.Book.id)
    if q:
        books = books.filter(m.Book.label.like(f"{q}"))

    pagination = create_pagination(total=books.count())

    return render_template(
        "book/index.html",
        books=books.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.NewBookForm()
    if form.validate_on_submit():
        book = m.Book(
            label=form.label.data,
        )
        log(log.INFO, "Form submitted. User: [%s]", book)
        flash("Book added!", "success")
        book.save()
        return redirect(url_for("book.get_all"))


@bp.route("/<int:book_id>", methods=["GET"])
def collection_view(book_id):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    else:
        return render_template("book/collection_view.html", book=book)


@bp.route("/<int:book_id>/about", methods=["GET"])
def about(book_id):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    else:
        return render_template("book/about_book.html", book=book)


@bp.route("/<int:book_id>/<int:collection_id>", methods=["GET"])
def sub_collection_view(book_id, collection_id):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    if collection.is_leaf:
        return render_template(
            "book/section_view.html",
            book=book,
            collection=collection,
            sub_collection=collection,
        )
    else:
        return render_template(
            "book/sub_collection_view.html", book=book, collection=collection
        )


@bp.route("/<int:book_id>/<int:collection_id>/about", methods=["GET"])
def about_collection(book_id, collection_id):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    else:
        return render_template(
            "book/about_collection.html", book=book, collection=collection
        )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/about", methods=["GET"]
)
def about_sub_collection(book_id, collection_id, sub_collection_id):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    sub_collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))

    else:
        return render_template(
            "book/about_sub_collection.html",
            book=book,
            collection=collection,
            sub_collection=sub_collection,
        )


@bp.route("/<int:book_id>/<int:collection_id>/<int:sub_collection_id>", methods=["GET"])
def section_view(book_id, collection_id, sub_collection_id):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
    if not collection:
        log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    else:
        return render_template(
            "book/section_view.html",
            book=book,
            collection=collection,
            sub_collection=sub_collection,
        )
