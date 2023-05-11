from flask_login import current_user
from flask import Response, flash, redirect, url_for, request

from app import models as m, db
from app.logger import log


class BookRouteVerifier:
    _routes = []

    @classmethod
    def add_route(cls, route_name: str):
        cls._routes.append(route_name)

    @classmethod
    def remove_route(cls, route_name: str):
        cls._routes.remove(route_name)

    @classmethod
    def is_present(cls, route_name: str) -> bool:
        return route_name in cls._routes


def register_book_verify_route(blueprint_name: str):
    def decorator(func: callable):
        BookRouteVerifier.add_route(f"{blueprint_name}.{func.__name__}")
        return func

    return decorator


def book_validator() -> Response | None:
    if not BookRouteVerifier.is_present(request.endpoint):
        return None

    request_args = (
        {**request.view_args, **request.args} if request.view_args else {**request.args}
    )

    book_id = request_args.get("book_id")
    if book_id:
        book: m.Book = db.session.get(m.Book, book_id)
        if not book or book.is_deleted or book.owner != current_user:
            log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
            flash("You are not owner of this book!", "danger")
            return redirect(url_for("book.my_books"))

    collection_id = request_args.get("collection_id")
    if collection_id:
        collection: m.Collection = db.session.get(m.Collection, collection_id)
        if not collection or collection.is_deleted:
            log(log.WARNING, "Collection with id [%s] not found", collection_id)
            flash("Collection not found", "danger")
            return redirect(url_for("book.collection_view", book_id=book_id))

    sub_collection_id = request_args.get("sub_collection_id")
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