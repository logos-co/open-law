from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required, current_user

from app.controllers import create_pagination
from app import models as m, db, forms as f
from app.logger import log

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route("/all", methods=["GET"])
def get_all():
    q = request.args.get("q", type=str, default=None)
    books: m.Book = m.Book.query.order_by(m.Book.id)
    if q:
        books = books.filter(m.Book.label.like(f"{q}"))

    pagination = create_pagination(total=books.count())

    return render_template(
        "book/index.html",
        books=books.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        search_query=q,
        all_books=True,
    )


@bp.route("/", methods=["GET"])
def my_books():
    q = request.args.get("q", type=str, default=None)
    books: m.Book = m.Book.query.order_by(m.Book.id)
    books = books.filter_by(user_id=current_user.id)
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
    form = f.CreateBookForm()
    if form.validate_on_submit():
        book: m.Book = m.Book(label=form.label.data, user_id=current_user.id)
        log(log.INFO, "Form submitted. Book: [%s]", book)
        book.save()
        m.BookVersion(semver="1.0.0", book_id=book.id).save()

        flash("Book added!", "success")
        return redirect(url_for("book.my_books"))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.my_books"))


@bp.route("/<int:book_id>", methods=["GET"])
def collection_view(book_id: int):
    book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))
    else:
        return render_template("book/collection_view.html", book=book)


@bp.route("/<int:book_id>/<int:collection_id>", methods=["GET"])
def sub_collection_view(book_id: int, collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))
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


@bp.route("/<int:book_id>/<int:collection_id>/<int:sub_collection_id>", methods=["GET"])
def section_view(book_id: int, collection_id: int, sub_collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
    if not sub_collection:
        log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
        flash("Sub_collection not found", "danger")
        return redirect(
            url_for(
                "book.sub_collection_view", book_id=book_id, collection_id=collection_id
            )
        )
    else:
        return render_template(
            "book/section_view.html",
            book=book,
            collection=collection,
            sub_collection=sub_collection,
        )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>",
    methods=["GET"],
)
def interpretation_view(
    book_id: int, collection_id: int, sub_collection_id: int, section_id: int
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
    if not sub_collection:
        log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
        flash("Sub_collection not found", "danger")
        return redirect(
            url_for(
                "book.sub_collection_view", book_id=book_id, collection_id=collection_id
            )
        )

    section: m.Section = db.session.get(m.Section, section_id)
    if not section:
        log(log.WARNING, "Section with id [%s] not found", section_id)
        flash("Section not found", "danger")
        return redirect(
            url_for(
                "book.section_view",
                book_id=book_id,
                collection_id=collection_id,
                sub_collection_id=sub_collection_id,
            )
        )
    else:
        return render_template(
            "book/interpretation_view.html",
            book=book,
            collection=collection,
            sub_collection=sub_collection,
            section=section,
        )


@bp.route("/<int:book_id>/settings", methods=["GET"])
@login_required
def settings(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)

    return render_template(
        "book/settings.html", book=book, roles=m.BookContributor.Roles
    )


@bp.route("/<int:book_id>/add_contributor", methods=["POST"])
@login_required
def add_contributor(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.owner != current_user:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_books"))

    form = f.AddContributorForm()

    if form.validate_on_submit():
        book_contributor = m.BookContributor.query.filter_by(
            user_id=form.user_id.data, book_id=book_id
        ).first()
        if book_contributor:
            log(log.INFO, "Contributor: [%s] already exists", book_contributor)
            flash("Already exists!", "danger")
            return redirect(url_for("book.settings", book_id=book_id))

        role = m.BookContributor.Roles(int(form.role.data))
        contributor = m.BookContributor(
            user_id=form.user_id.data, book_id=book_id, role=role
        )
        log(log.INFO, "New contributor [%s]", contributor)
        contributor.save()

        flash("Contributor was added!", "success")
        return redirect(url_for("book.settings", book_id=book_id))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.settings", book_id=book_id))


@bp.route("/<int:book_id>/delete_contributor", methods=["POST"])
@login_required
def delete_contributor(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.owner != current_user:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_books"))

    form = f.DeleteContributorForm()

    if form.validate_on_submit():
        book_contributor = m.BookContributor.query.filter_by(
            user_id=int(form.user_id.data), book_id=book.id
        ).first()
        if not book_contributor:
            log(
                log.INFO,
                "BookContributor does not exists user: [%s], book: [%s]",
                form.user_id.data,
                book.id,
            )
            flash("Does not exists!", "success")
            return redirect(url_for("book.settings", book_id=book_id))

        log(log.INFO, "Delete BookContributor [%s]", book_contributor)
        db.session.delete(book_contributor)
        db.session.commit()

        flash("Success!", "success")
        return redirect(url_for("book.settings", book_id=book_id))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.settings", book_id=book_id))


@bp.route("/<int:book_id>/edit_contributor_role", methods=["POST"])
@login_required
def edit_contributor_role(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.owner != current_user:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_books"))

    form = f.EditContributorRoleForm()

    if form.validate_on_submit():
        book_contributor = m.BookContributor.query.filter_by(
            user_id=int(form.user_id.data), book_id=book.id
        ).first()
        if not book_contributor:
            log(
                log.INFO,
                "BookContributor does not exists user: [%s], book: [%s]",
                form.user_id.data,
                book.id,
            )
            flash("Does not exists!", "success")
            return redirect(url_for("book.settings", book_id=book_id))

        role = m.BookContributor.Roles(int(form.role.data))
        book_contributor.role = role

        log(
            log.INFO,
            "Update contributor [%s] role: new role: [%s]",
            book_contributor,
            role,
        )
        book_contributor.save()

        flash("Success!", "success")
        return redirect(url_for("book.settings", book_id=book_id))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.settings", book_id=book_id))
