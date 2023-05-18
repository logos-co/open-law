from flask.testing import FlaskCliRunner
from click.testing import Result
from app import models as m


def test_dummy_data(runner: FlaskCliRunner):
    res: Result = runner.invoke(args=["db-populate"])
    assert "Dummy data added" in res.output, res.stderr

    user: m.User = m.User.query.filter_by(username="Dummy User 1").first()
    book: m.Book = m.Book.query.filter_by(label="Dummy Book").first()

    assert user
    assert user.books
    assert book in user.books

    # stars
    book_star: m.BookStar = m.BookStar.query.first()
    assert book.stars
    assert user.stars
    assert book_star
    assert book_star.user_id == user.id
    assert book_star.book_id == book.id

    # contributors
    assert book.contributors
    assert len(book.contributors) == 2

    moderator: m.User = m.User.query.filter_by(username="Dummy Moderator").first()
    book_moderator: m.BookContributor = m.BookContributor.query.filter_by(
        role=m.BookContributor.Roles.MODERATOR
    ).first()

    assert book_moderator
    assert book_moderator.book_id == book.id
    assert book_moderator.user_id == moderator.id

    editor: m.User = m.User.query.filter_by(username="Dummy Editor").first()
    book_editor: m.BookContributor = m.BookContributor.query.filter_by(
        role=m.BookContributor.Roles.EDITOR
    ).first()
    assert book_editor
    assert book_editor.book_id == book.id
    assert book_editor.user_id == editor.id

    # versions
    assert book.versions

    exported_version: m.BookVersion = m.BookVersion.query.filter_by(
        book=book, exported=True
    ).first()
    assert exported_version.exported
    assert exported_version.book_id == book.id
    assert not exported_version.derivative_id

    unexported_version: m.BookVersion = m.BookVersion.query.filter_by(
        book=book, exported=False
    ).first()
    assert not unexported_version.exported
    assert unexported_version.derivative == exported_version
    assert unexported_version.book_id == book.id

    # collections

    # root
    #   - collection 1 (leaf)
    #   - collection 2
    #       - subcollection 2.1 (leaf)

    root_collection: m.Collection = m.Collection.query.filter_by(
        label="Dummy Root Collection Label"
    ).first()

    assert root_collection
    assert root_collection.is_root
    assert not root_collection.is_leaf
    assert root_collection.version == unexported_version

    collection_1: m.Collection = m.Collection.query.filter_by(
        label="Dummy Collection 1 Label"
    ).first()

    assert collection_1
    assert not collection_1.is_root
    assert collection_1.is_leaf
    assert collection_1.version == unexported_version

    collection_2: m.Collection = m.Collection.query.filter_by(
        label="Dummy Collection 2 Label"
    ).first()

    assert collection_2
    assert not collection_2.is_leaf
    assert not collection_2.is_root
    assert collection_2.version == unexported_version

    subcollection_2_1: m.Collection = m.Collection.query.filter_by(
        label="Dummy SubCollection 2.1 Label"
    ).first()

    assert subcollection_2_1
    assert subcollection_2_1.is_leaf
    assert not subcollection_2_1.is_root

    # root
    #   - collection 1 (leaf)
    #       - section 1.1
    #   - collection 2
    #       - subcollection 2.1 (leaf)
    #           - section 2.1.1
    #           - section 2.1.2

    section_1_1: m.Section = m.Section.query.filter_by(
        label="Dummy Section 1.1 Label"
    ).first()

    assert section_1_1
    assert section_1_1.user == user
    assert section_1_1.collection == collection_1

    section_2_1_1: m.Section = m.Section.query.filter_by(
        label="Dummy Section 2.1.1 Label"
    ).first()

    assert section_2_1_1
    assert section_2_1_1.user == user
    assert section_2_1_1.collection == subcollection_2_1

    section_2_1_2: m.Section = m.Section.query.filter_by(
        label="Dummy Section 2.1.2 Label"
    ).first()

    assert section_2_1_2
    assert section_2_1_2.user == user
    assert section_2_1_2.collection == subcollection_2_1

    # interpretations

    # root
    #   - collection 1 (leaf)
    #       - section 1.1
    #           - interpretation 1
    #   - collection 2
    #       - subcollection 2.1 (leaf)
    #           - section 2.1.1
    #               - interpretation 2 (marked)
    #           - section 2.1.2
    #               - interpretation 3 (marked)
    #               - interpretation 4

    interpretation_1: m.Interpretation = m.Interpretation.query.filter_by(
        text="Dummy Interpretation 1 About"
    ).first()

    assert interpretation_1
    assert interpretation_1.user == user
    assert interpretation_1.section == section_1_1

    interpretation_2: m.Interpretation = m.Interpretation.query.filter_by(
        text="Dummy Interpretation 2 About"
    ).first()

    assert interpretation_2
    assert interpretation_2.marked
    assert interpretation_2.user == user
    assert interpretation_2.section == section_2_1_1

    interpretation_3: m.Interpretation = m.Interpretation.query.filter_by(
        text="Dummy Interpretation 3 About"
    ).first()

    assert interpretation_3
    assert interpretation_3.marked
    assert interpretation_3.user == user
    assert interpretation_3.section == section_2_1_2

    interpretation_4: m.Interpretation = m.Interpretation.query.filter_by(
        text="Dummy Interpretation 3 About"
    ).first()

    assert interpretation_4
    assert interpretation_4.user == user
    assert interpretation_4.section == section_2_1_2

    # comments
    # - interpretation 2
    #   - comment 1
    #       - comment 1.1
    #       - comment 1.2 (marked)
    #   - comment 2
    #   - comment 3
    #       - comment 3.1 (marked)
    #       - comment 3.2 (approved)
    #       - comment 3.3

    comment_1: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 1 Text"
    ).first()

    assert not comment_1.parent

    comment_1_1: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 1.1 Text"
    ).first()

    comment_1_2: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 1.2 Text"
    ).first()

    assert comment_1_1 in comment_1.children
    assert comment_1_1 in comment_1.children
    assert comment_1_2.parent == comment_1
    assert comment_1_2.parent == comment_1
    assert comment_1_2.marked

    comment_2: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 2 Text"
    ).first()

    assert not comment_2.parent
    assert not comment_2.children

    comment_3: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 3 Text"
    ).first()

    assert not comment_3.parent
    assert comment_3.children

    comment_3_1: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 3.1 Text"
    ).first()

    comment_3_2: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 3.2 Text"
    ).first()

    comment_3_3: m.Comment = m.Comment.query.filter_by(
        text="Dummy Comment 3.3 Text"
    ).first()

    assert comment_3_1 in comment_3.children
    assert comment_3_2 in comment_3.children
    assert comment_3_3 in comment_3.children
    assert comment_3_1.marked
    assert comment_3_2.approved

    assert comment_1 in interpretation_2.comments
    assert comment_2 in interpretation_2.comments
    assert comment_3 in interpretation_2.comments

    # - comment 3.1 (2 positive, 2 negative)
    # - comment 3.2 (1 negative)
    # - comment 3.3 (1 positive)

    assert len(comment_3_1.votes) == 4
    assert len(comment_3_2.votes) == 1
    assert len(comment_3_3.votes) == 1

    # - interpretation 1 (2 positive, 1 negative)
    # - interpretation 2 (1 negative)
    # - interpretation 3 (1 positive)
    assert len(interpretation_1.votes) == 3
    assert len(interpretation_2.votes) == 1
    assert len(interpretation_3.votes) == 1

    # interpretation tags
    #   - tags: 1,
    # - interpretation 2
    #   - tags: 2, 3
    # - interpretation 3
    #   - tags: 1, 3
    assert len(interpretation_1.tags) == 1
    assert len(interpretation_2.tags) == 2
    assert len(interpretation_3.tags) == 2

    # # - comment 1
    # #   - tags: 1,
    # # - comment 2
    # #   - tags: 2, 3
    # # - comment 3
    # #   - tags: 1, 3
    # assert len(comment_1.tags) == 1
    # assert len(comment_2.tags) == 2
    # assert len(comment_3.tags) == 2
