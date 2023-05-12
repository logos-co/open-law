from app import models as m

from random import randint

TEST_ADMIN_NAME = "bob"
TEST_ADMIN_EMAIL = "bob@test.com"
TEST_ADMIN_PASSWORD = "password"


def create(username=TEST_ADMIN_NAME, password=TEST_ADMIN_PASSWORD):
    user = m.User(username=username)
    user.password = password
    user.save()
    return user.id


def login(client, username=TEST_ADMIN_NAME, password=TEST_ADMIN_PASSWORD):
    user = m.User.query.filter_by(username=username).first()
    response = client.post(
        "/login", data=dict(user_id=username, password=password), follow_redirects=True
    )
    return response, user


def logout(client):
    return client.get("/logout", follow_redirects=True)


def create_test_book(owner_id: int, entity_id: int = randint(1, 100)):
    book: m.Book = m.Book(
        label=f"Book {entity_id}", about=f"About {entity_id}", user_id=owner_id
    ).save()

    version: m.BookVersion = m.BookVersion(semver="1.0.0", book_id=book.id).save()

    collection: m.Collection = m.Collection(
        label=f"Collection {entity_id}", version_id=version.id
    ).save()

    section: m.Section = m.Section(
        label=f"Section {entity_id}",
        user_id=owner_id,
        collection_id=collection.id,
        version_id=version.id,
    ).save()

    interpretation: m.Interpretation = m.Interpretation(
        section_id=section.id,
        label=f"Interpretation {entity_id}",
        text=f"Interpretation Text {entity_id}",
        user_id=owner_id,
    ).save()

    m.Comment(
        text=f"Comment {entity_id}",
        user_id=owner_id,
        interpretation_id=interpretation.id,
    ).save()
