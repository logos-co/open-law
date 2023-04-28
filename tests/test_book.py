from flask import current_app as Response
from flask.testing import FlaskClient, FlaskCliRunner

from app import models as m, db
from tests.utils import login


def test_create_book(client: FlaskClient):
    login(client)

    BOOK_NAME = "Test Book"

    # label len < 6
    response: Response = client.post(
        "/book/create",
        data=dict(
            label="12345",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Label must be between 6 and 256 characters long." in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert not book
    assert not m.Book.query.count()

    # label len > 256
    response: Response = client.post(
        "/book/create",
        data=dict(
            label="".join(["0" for _ in range(1025)]),
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Label must be between 6 and 256 characters long." in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert not book
    assert not m.Book.query.count()

    response: Response = client.post(
        "/book/create",
        data=dict(
            label=BOOK_NAME,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Book added!" in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert book
    assert book.versions
    assert len(book.versions) == 1


def test_add_contributor(client: FlaskClient):
    _, user = login(client)
    user: m.User

    moderator = m.User(username="Moderator", password="test").save()

    moderators_book = m.Book(label="Test Book", user_id=moderator.id).save()
    response: Response = client.post(
        f"/book/{moderators_book.id}/add_contributor",
        data=dict(user_id=moderator.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You are not owner of this book!" in response.data

    book = m.Book(label="Test Book", user_id=user.id).save()

    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=moderator.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Contributor was added!" in response.data
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=moderator.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Already exists!" in response.data

    contributor: m.BookContributor = m.BookContributor.query.filter_by(
        user=moderator, book=book
    ).first()
    assert contributor.role == m.BookContributor.Roles.MODERATOR
    assert len(book.contributors) == 1

    editor = m.User(username="Editor", password="test").save()
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=editor.id, role=m.BookContributor.Roles.EDITOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Contributor was added!" in response.data

    contributor: m.BookContributor = m.BookContributor.query.filter_by(
        user=editor, book=book
    ).first()
    assert contributor.role == m.BookContributor.Roles.EDITOR
    assert len(book.contributors) == 2


def test_delete_contributor(client: FlaskClient, runner: FlaskCliRunner):
    _, user = login(client)
    user: m.User

    # add dummmy data
    runner.invoke(args=["db-populate"])

    book = db.session.get(m.Book, 1)
    book.user_id = user.id
    book.save()

    contributors_len = len(book.contributors)
    assert contributors_len

    contributor_to_delete = book.contributors[0]

    response: Response = client.post(
        f"/book/{book.id}/delete_contributor",
        data=dict(user_id=contributor_to_delete.user_id),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    response: Response = client.post(
        f"/book/{book.id}/delete_contributor",
        data=dict(user_id=contributor_to_delete.user_id),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Does not exists!" in response.data


def test_edit_contributor_role(client: FlaskClient, runner: FlaskCliRunner):
    _, user = login(client)
    user: m.User

    # add dummmy data
    runner.invoke(args=["db-populate"])

    book = db.session.get(m.Book, 1)
    book.user_id = user.id
    book.save()

    contributors_len = len(book.contributors)
    assert contributors_len

    contributor_edit = book.contributors[0]

    assert contributor_edit.role == m.BookContributor.Roles.MODERATOR

    response: Response = client.post(
        f"/book/{book.id}/edit_contributor_role",
        data=dict(
            user_id=contributor_edit.user_id,
            role=m.BookContributor.Roles.MODERATOR.value,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data


def test_crud_collection(client: FlaskClient, runner: FlaskCliRunner):
    _, user = login(client)
    user: m.User

    # add dummmy data
    runner.invoke(args=["db-populate"])

    book = db.session.get(m.Book, 1)
    book.user_id = user.id
    book.save()

    response: Response = client.post(
        f"/book/{book.id}/create_collection",
        data=dict(label="Test Collection #1 Label", about="Test Collection #1 About"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    response: Response = client.post(
        f"/book/{book.id}/create_collection",
        data=dict(label="Test Collection #1 Label", about="Test Collection #1 About"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection label must be unique!" in response.data

    collection: m.Collection = m.Collection.query.filter_by(
        label="Test Collection #1 Label"
    ).first()
    m.Collection(
        label="Test Collection #2 Label",
        version_id=collection.version_id,
        parent_id=collection.parent_id,
    ).save()

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/edit",
        data=dict(
            label="Test Collection #2 Label",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection label must be unique!" in response.data

    new_label = "Test Collection #1 Label(edited)"
    new_about = "Test Collection #1 About(edited)"

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/edit",
        data=dict(
            label=new_label,
            about=new_about,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    edited_collection: m.Collection = m.Collection.query.filter_by(
        label=new_label, about=new_about
    ).first()
    assert edited_collection

    response: Response = client.post(
        f"/book/{book.id}/999/edit",
        data=dict(
            label=new_label,
            about=new_about,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection not found" in response.data

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    deleted_collection: m.Collection = db.session.get(m.Collection, collection.id)
    assert deleted_collection.is_deleted

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection not found" in response.data


def test_crud_subcollection(client: FlaskClient, runner: FlaskCliRunner):
    _, user = login(client)
    user: m.User

    # add dummmy data
    runner.invoke(args=["db-populate"])

    book: m.Book = db.session.get(m.Book, 1)
    book.user_id = user.id
    book.save()

    leaf_collection: m.Collection = m.Collection(
        label="Test Leaf Collection #1 Label",
        version_id=book.versions[-1].id,
        is_leaf=True,
        parent_id=book.versions[-1].root_collection.id,
    ).save()
    collection: m.Collection = m.Collection(
        label="Test Collection #1 Label", version_id=book.versions[-1].id
    ).save()

    response: Response = client.post(
        f"/book/{book.id}/{leaf_collection.id}/create_sub_collection",
        data=dict(
            label="Test SubCollection #1 Label", about="Test SubCollection #1 About"
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You can't create subcollection for this collection" in response.data

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/create_sub_collection",
        data=dict(
            label="Test SubCollection #1 Label", about="Test SubCollection #1 About"
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/create_sub_collection",
        data=dict(
            label="Test SubCollection #1 Label", about="Test SubCollection #1 About"
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection label must be unique!" in response.data

    sub_collection: m.Collection = m.Collection.query.filter_by(
        label="Test SubCollection #1 Label"
    ).first()
    assert sub_collection
    assert sub_collection.is_leaf
    assert sub_collection.parent_id == collection.id

    m.Collection(
        label="Test SubCollection #2 Label",
        version_id=collection.version_id,
        parent_id=collection.id,
    ).save()

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{sub_collection.id}/edit",
        data=dict(
            label="Test SubCollection #2 Label",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection label must be unique!" in response.data

    new_label = "Test SubCollection #1 Label(edited)"
    new_about = "Test SubCollection #1 About(edited)"

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{sub_collection.id}/edit",
        data=dict(
            label=new_label,
            about=new_about,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    edited_collection: m.Collection = m.Collection.query.filter_by(
        label=new_label, about=new_about
    ).first()
    assert edited_collection

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/9999/edit",
        data=dict(
            label=new_label,
            about=new_about,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"SubCollection not found" in response.data

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{sub_collection.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    deleted_collection: m.Collection = db.session.get(m.Collection, sub_collection.id)
    assert deleted_collection.is_deleted

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{sub_collection.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Collection not found" in response.data
