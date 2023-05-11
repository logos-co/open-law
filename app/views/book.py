from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required, current_user

from app.controllers import (
    create_pagination,
    create_breadcrumbs,
    register_book_verify_route,
    book_validator,
)
from app import models as m, db, forms as f
from app.logger import log

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.before_request
def before_request():
    if response := book_validator():
        return response


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


@bp.route("/", methods=["GET"])
@login_required
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
        version = m.BookVersion(semver="1.0.0", book_id=book.id).save()
        m.Collection(
            label="Root Collection", version_id=version.id, is_root=True
        ).save()

        flash("Book added!", "success")
        return redirect(url_for("book.my_books"))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.my_books"))


@bp.route("/<int:book_id>/edit", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def edit(book_id: int):
    form = f.EditBookForm()
    if form.validate_on_submit():
        book: m.Book = db.session.get(m.Book, book_id)
        label = form.label.data

        book.label = label
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


@bp.route("/<int:book_id>/collections", methods=["GET"])
def collection_view(book_id: int):
    book = db.session.get(m.Book, book_id)
    breadcrumbs = create_breadcrumbs(book_id=book_id, collection_path=())
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))
    else:
        return render_template(
            "book/collection_view.html", book=book, breadcrumbs=breadcrumbs
        )


@bp.route("/<int:book_id>/<int:collection_id>/subcollections", methods=["GET"])
def sub_collection_view(book_id: int, collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))
    breadcrumbs = create_breadcrumbs(book_id=book_id, collection_path=(collection.id,))
    if collection.is_leaf:
        return redirect(
            url_for("book.section_view", book_id=book.id, collection_id=collection.id)
        )
    else:
        return render_template(
            "book/sub_collection_view.html",
            book=book,
            collection=collection,
            breadcrumbs=breadcrumbs,
        )


@bp.route("/<int:book_id>/<int:collection_id>/sections", methods=["GET"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/sections",
    methods=["GET"],
)
def section_view(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    sub_collection = None
    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
        if not sub_collection or sub_collection.is_deleted:
            log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
            flash("Sub_collection not found", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

    if sub_collection:
        sections = sub_collection.active_sections
    else:
        sections = collection.active_sections

    breadcrumbs = create_breadcrumbs(
        book_id=book_id,
        collection_path=(
            collection_id,
            sub_collection_id,
        ),
    )

    return render_template(
        "book/section_view.html",
        book=book,
        collection=collection,
        sections=sections,
        sub_collection=sub_collection,
        breadcrumbs=breadcrumbs,
    )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/interpretations",
    methods=["GET"],
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/interpretations",
    methods=["GET"],
)
def interpretation_view(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
        if not sub_collection or sub_collection.is_deleted:
            log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
            flash("Sub_collection not found", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
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
        breadcrumbs = create_breadcrumbs(
            book_id=book_id,
            collection_path=(
                collection_id,
                sub_collection_id,
            ),
            section_id=section_id,
        )
        return render_template(
            "book/interpretation_view.html",
            book=book,
            collection=collection,
            sub_collection=sub_collection if sub_collection_id else None,
            section=section,
            breadcrumbs=breadcrumbs,
        )


@bp.route("/<int:book_id>/settings", methods=["GET"])
@register_book_verify_route(bp.name)
@login_required
def settings(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)

    return render_template(
        "book/settings.html", book=book, roles=m.BookContributor.Roles
    )


@bp.route("/<int:book_id>/add_contributor", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def add_contributor(book_id: int):
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
@register_book_verify_route(bp.name)
@login_required
def delete_contributor(book_id: int):
    form = f.DeleteContributorForm()

    if form.validate_on_submit():
        book_contributor = m.BookContributor.query.filter_by(
            user_id=int(form.user_id.data), book_id=book_id
        ).first()
        if not book_contributor:
            log(
                log.INFO,
                "BookContributor does not exists user: [%s], book: [%s]",
                form.user_id.data,
                book_id,
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
@register_book_verify_route(bp.name)
@login_required
def edit_contributor_role(book_id: int):
    form = f.EditContributorRoleForm()

    if form.validate_on_submit():
        book_contributor = m.BookContributor.query.filter_by(
            user_id=int(form.user_id.data), book_id=book_id
        ).first()
        if not book_contributor:
            log(
                log.INFO,
                "BookContributor does not exists user: [%s], book: [%s]",
                form.user_id.data,
                book_id,
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


###############################
# Collection/SubCollection CRUD
###############################


@bp.route("/<int:book_id>/create_collection", methods=["POST"])
@bp.route("/<int:book_id>/<int:collection_id>/create_sub_collection", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def collection_create(book_id: int, collection_id: int | None = None):
    book: m.Book = db.session.get(m.Book, book_id)

    redirect_url = url_for("book.collection_view", book_id=book_id)
    if collection_id:
        collection: m.Collection = db.session.get(m.Collection, collection_id)
        if collection.is_leaf:
            log(log.WARNING, "Collection with id [%s] is leaf", collection_id)
            flash("You can't create subcollection for this collection", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

        redirect_url = url_for(
            "book.sub_collection_view", book_id=book_id, collection_id=collection_id
        )

    form = f.CreateCollectionForm()

    if form.validate_on_submit():
        label = form.label.data
        collection: m.Collection = m.Collection.query.filter_by(
            is_deleted=False,
            label=label,
        )
        if collection_id:
            collection = collection.filter_by(parent_id=collection_id)
        else:
            collection = collection.filter_by(
                parent_id=book.versions[-1].root_collection.id
            )
        collection = collection.first()

        if collection:
            log(
                log.INFO,
                "Collection with similar label already exists. Book: [%s], Collection: [%s], Label: [%s]",
                book.id,
                collection.id,
                label,
            )
            flash("Collection label must be unique!", "danger")
            return redirect(redirect_url)

        collection: m.Collection = m.Collection(
            label=label,
            about=form.about.data,
            parent_id=book.versions[-1].root_collection.id,
        )
        if collection_id:
            collection.parent_id = collection_id
            collection.is_leaf = True

        log(log.INFO, "Create collection [%s]. Book: [%s]", collection, book.id)
        collection.save()

        flash("Success!", "success")
        if collection_id:
            redirect_url = url_for(
                "book.sub_collection_view", book_id=book_id, collection_id=collection_id
            )
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Collection/Subcollection create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route("/<int:book_id>/<int:collection_id>/edit", methods=["POST"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/edit", methods=["POST"]
)
@register_book_verify_route(bp.name)
@login_required
def collection_edit(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if sub_collection_id:
        collection = db.session.get(m.Collection, sub_collection_id)

    form = f.EditCollectionForm()
    redirect_url = url_for(
        "book.sub_collection_view",
        book_id=book_id,
        collection_id=collection_id,
    )

    if form.validate_on_submit():
        label = form.label.data
        collection_query: m.Collection = m.Collection.query.filter_by(
            is_deleted=False,
            label=label,
        ).filter(m.Collection.id != collection.id)

        if sub_collection_id:
            collection_query = collection_query.filter_by(parent_id=collection_id)
        else:
            collection_query = collection_query.filter_by(
                parent_id=collection.parent.id
            )

        if collection_query.first():
            log(
                log.INFO,
                "Collection with similar label already exists. Book: [%s], Collection: [%s], Label: [%s]",
                book.id,
                collection_id,
                label,
            )
            flash("Collection label must be unique!", "danger")
            return redirect(redirect_url)

        if label:
            collection.label = label

        about = form.about.data
        if about:
            collection.about = about

        log(log.INFO, "Edit collection [%s]", collection.id)
        collection.save()

        flash("Success!", "success")
        if sub_collection_id:
            redirect_url = url_for(
                "book.section_view",
                book_id=book_id,
                collection_id=collection_id,
                sub_collection_id=sub_collection_id,
            )
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Collection edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route("/<int:book_id>/<int:collection_id>/delete", methods=["POST"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/delete",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def collection_delete(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if sub_collection_id:
        collection: m.Collection = db.session.get(m.Collection, sub_collection_id)

    collection.is_deleted = True

    log(log.INFO, "Delete collection [%s]", collection.id)
    collection.save()

    flash("Success!", "success")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )


###############
# Sections CRUD
###############


@bp.route("/<int:book_id>/<int:collection_id>/create_section", methods=["POST"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/create_section",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def section_create(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    sub_collection = None
    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)

    redirect_url = url_for("book.collection_view", book_id=book_id)
    if collection_id:
        redirect_url = url_for(
            "book.section_view",
            book_id=book_id,
            collection_id=collection_id,
            sub_collection_id=sub_collection_id,
        )

    form = f.CreateSectionForm()

    if form.validate_on_submit():
        section: m.Section = m.Section(
            label=form.label.data,
            about=form.about.data,
            collection_id=sub_collection_id or collection_id,
            version_id=book.last_version.id,
        )
        if sub_collection:
            sub_collection.is_leaf = True
        else:
            collection.is_leaf = True
        log(log.INFO, "Create section [%s]. Collection: [%s]", section, collection_id)
        section.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Section create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/edit_section", methods=["POST"]
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/edit_section",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def section_edit(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    redirect_url = url_for(
        "book.interpretation_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
    )
    section: m.Section = db.session.get(m.Section, section_id)

    form = f.EditSectionForm()

    if form.validate_on_submit():
        label = form.label.data
        if label:
            section.label = label

        about = form.about.data
        if about:
            section.about = about

        log(log.INFO, "Edit section [%s]", section.id)
        section.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Section edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/delete_section",
    methods=["POST"],
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/delete_section",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def section_delete(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    collection: m.Collection = db.session.get(
        m.Collection, sub_collection_id or collection_id
    )
    section: m.Section = db.session.get(m.Section, section_id)

    section.is_deleted = True
    if not collection.active_sections:
        log(
            log.INFO,
            "Section [%s] has no active section. Set is_leaf = False",
            section.id,
        )
        collection.is_leaf = False

    log(log.INFO, "Delete section [%s]", section.id)
    section.save()

    flash("Success!", "success")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )


#####################
# Interpretation CRUD
#####################


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/create_interpretation",
    methods=["POST"],
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/create_interpretation",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def interpretation_create(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    section: m.Section = db.session.get(m.Section, section_id)
    form = f.CreateInterpretationForm()
    redirect_url = url_for(
        "book.interpretation_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section.id,
    )

    if form.validate_on_submit():
        interpretation: m.Interpretation = m.Interpretation(
            label=form.label.data,
            text=form.text.data,
            section_id=section_id,
            user_id=current_user.id,
        )
        log(
            log.INFO,
            "Create interpretation [%s]. Section: [%s]",
            interpretation,
            section,
        )
        interpretation.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Interpretation create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/edit_interpretation",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/edit_interpretation"
    ),
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def interpretation_edit(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    form = f.EditInterpretationForm()
    redirect_url = url_for(
        "book.qa_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
        interpretation_id=interpretation_id,
    )

    if form.validate_on_submit():
        label = form.label.data
        if label:
            interpretation.label = label

        interpretation.text = form.text.data

        log(log.INFO, "Edit interpretation [%s]", interpretation.id)
        interpretation.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Interpretation edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/delete_interpretation",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/delete_interpretation"
    ),
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def interpretation_delete(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )

    interpretation.is_deleted = True
    log(log.INFO, "Delete interpretation [%s]", interpretation)
    interpretation.save()

    flash("Success!", "success")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/preview",
    methods=["GET"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/preview"
    ),
    methods=["GET"],
)
@login_required
def qa_view(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
        if not sub_collection or sub_collection.is_deleted:
            log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
            flash("SubCollection not found", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

    redirect_url = url_for(
        "book.interpretation_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
    )
    section: m.Section = db.session.get(m.Section, section_id)
    if not section or section.is_deleted:
        log(log.WARNING, "Section with id [%s] not found", section_id)
        flash("Section not found", "danger")
        return redirect(redirect_url)

    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    if not interpretation or interpretation.is_deleted:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        flash("Interpretation not found", "danger")
        return redirect(redirect_url)

    breadcrumbs = create_breadcrumbs(
        book_id=book_id,
        collection_path=(
            collection_id,
            sub_collection_id,
        ),
        section_id=section_id,
        interpretation_id=interpretation.id,
    )
    return render_template(
        "book/qa_view.html",
        book=book,
        collection=collection,
        sub_collection=sub_collection if sub_collection_id else None,
        section=section,
        interpretation=interpretation,
        breadcrumbs=breadcrumbs,
    )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/preview/create_comment",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/preview/create_comment"
    ),
    methods=["POST"],
)
@login_required
def create_comment(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_books"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    sub_collection = None
    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
        if not sub_collection or sub_collection.is_deleted:
            log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
            flash("SubCollection not found", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

    breadcrumbs = create_breadcrumbs(
        book_id=book_id,
        collection_path=(
            collection_id,
            sub_collection_id,
        ),
        section_id=section_id,
        interpretation_id=interpretation_id,
    )

    redirect_url = url_for(
        "book.qa_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
        interpretation_id=interpretation_id,
        breadcrumbs=breadcrumbs,
    )
    section: m.Section = db.session.get(m.Section, section_id)
    if not section or section.is_deleted:
        log(log.WARNING, "Section with id [%s] not found", section_id)
        flash("Section not found", "danger")
        return redirect(redirect_url)

    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    if not interpretation or interpretation.is_deleted:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        flash("Interpretation not found", "danger")
        return redirect(redirect_url)

    form = f.CreateCommentForm()

    if form.validate_on_submit():
        comment: m.Comment = m.Comment(
            text=form.text.data,
            user_id=current_user.id,
            interpretation_id=interpretation_id,
        )
        if form.parent_id.data:
            comment.parent_id = form.parent_id.data
            comment.interpretation = None

        log(
            log.INFO,
            "Create comment for interpretation [%s]. Section: [%s]",
            interpretation,
            section,
        )
        comment.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Comment create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.lower().replace("field", field_label).title(), "danger")

        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/comment_delete",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/comment_delete"
    ),
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def comment_delete(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    form = f.DeleteCommentForm()
    comment_id = form.comment_id.data
    comment: m.Comment = db.session.get(m.Comment, comment_id)

    if form.validate_on_submit():
        comment.is_deleted = True
        log(log.INFO, "Delete comment [%s]", comment)
        comment.save()

        flash("Success!", "success")
        return redirect(
            url_for(
                "book.qa_view",
                book_id=book_id,
                collection_id=collection_id,
                sub_collection_id=sub_collection_id,
                section_id=section_id,
                interpretation_id=interpretation_id,
            )
        )
    return redirect(
        url_for(
            "book.sub_collection_view",
            book_id=book_id,
            collection_id=collection_id,
        )
    )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/comment_edit",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/comment_edit"
    ),
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def comment_edit(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    form = f.EditCommentForm()
    comment_id = form.comment_id.data
    comment: m.Comment = db.session.get(m.Comment, comment_id)

    if form.validate_on_submit():
        comment.text = form.text.data
        comment.edited = True
        log(log.INFO, "Delete comment [%s]", comment)
        comment.save()

        flash("Success!", "success")
        return redirect(
            url_for(
                "book.qa_view",
                book_id=book_id,
                collection_id=collection_id,
                sub_collection_id=sub_collection_id,
                section_id=section_id,
                interpretation_id=interpretation_id,
            )
        )
    return redirect(
        url_for(
            "book.sub_collection_view",
            book_id=book_id,
            collection_id=collection_id,
        )
    )
