from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app import models as m, db, forms as f
from app.logger import log

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route("/", methods=["GET"])
def get_all():
    # q = request.args.get("q", type=str, default=None)
    # books = m.Book.query.order_by(m.Book.id)
    # if q:
    #     books = books.filter(m.Book.label.like(f"{q}"))

    # pagination = create_pagination(total=books.count())

    # return render_template(
    #     "books/index.html",
    #     books=books.paginate(page=pagination.page, per_page=pagination.per_page),
    #     page=pagination,
    #     search_query=q,
    # )
    return render_template(
        "book/index.html",
    )


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.CreateBookForm()
    if form.validate_on_submit():
        book = m.Book(
            label=form.label.data,
        )
        log(log.INFO, "Form submitted. Book: [%s]", book)
        book.save()
        m.BookVersion(semver="1.0.0", book_id=book.id).save()

        flash("Book added!", "success")
        return redirect(url_for("book.get_all"))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.get_all"))


@bp.route("/<int:book_id>/settings", methods=["GET", "POST"])
@login_required
def settings(book_id):
    book: m.Book = db.session.get(m.Book, book_id)

    return render_template(
        "book/settings.html", book=book, roles=m.BookContributor.Roles
    )


@bp.route("/<int:book_id>/add_contributor", methods=["POST"])
@login_required
def add_contributor(book_id):
    # TODO replace redirects to book.edit/settings
    book: m.Book = db.session.get(m.Book, book_id)
    if book.owner != current_user:
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.get_all"))

    form = f.AddContributorForm()

    if form.validate_on_submit():
        book_contributor = m.BookContributor.query.filter_by(
            user_id=form.user_id.data, book_id=book_id
        ).first()
        if book_contributor:
            flash("Already exists!", "danger")
            return redirect(url_for("book.settings", book_id=book_id))

        role = m.BookContributor.Roles(int(form.role.data))
        m.BookContributor(user_id=form.user_id.data, book_id=book_id, role=role).save()

        flash("Contributor was added!", "success")
        return redirect(url_for("book.settings", book_id=book_id))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.settings", book_id=book_id))
