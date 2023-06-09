from app import models as m


def create_dummy_data():
    user = m.User(username="Dummy User 1", password="Dummy Password").save()
    user_2 = m.User(username="Dummy User 2", password="Dummy Password").save()
    user_3 = m.User(username="Dummy User 3", password="Dummy Password").save()
    user_4 = m.User(username="Dummy User 4", password="Dummy Password").save()

    book = m.Book(label="Dummy Book", user_id=user.id).save()

    m.BookStar(user_id=user.id, book_id=book.id).save()

    moderator = m.User(username="Dummy Moderator", password="Dummy Password").save()
    m.BookContributor(
        user_id=moderator.id, book_id=book.id, role=m.BookContributor.Roles.MODERATOR
    ).save()

    editor = m.User(username="Dummy Editor", password="Dummy Password").save()
    m.BookContributor(
        user_id=editor.id, book_id=book.id, role=m.BookContributor.Roles.EDITOR
    ).save()

    exported_version = m.BookVersion(
        semver="1.0.0", book_id=book.id, exported=True
    ).save()
    unexported_version = m.BookVersion(
        semver="1.0.1", book_id=book.id, exported=False, derivative=exported_version
    ).save()

    # collections

    # root
    #   - collection 1 (leaf)
    #   - collection 2
    #       - subcollection 2.1 (leaf)

    # root
    rool_collection = m.Collection(
        label="Dummy Root Collection Label",
        about="Dummy Root Collection About",
        is_root=True,
        version_id=unexported_version.id,
    ).save()

    collection_1 = m.Collection(
        label="Dummy Collection 1 Label",
        about="Dummy Collection 1 About",
        version_id=unexported_version.id,
        parent_id=rool_collection.id,
        is_leaf=True,
    ).save()

    collection_2 = m.Collection(
        label="Dummy Collection 2 Label",
        about="Dummy Collection 2 About",
        version_id=unexported_version.id,
        parent_id=rool_collection.id,
    ).save()

    subcollection_2_1 = m.Collection(
        label="Dummy SubCollection 2.1 Label",
        about="Dummy SubCollection 2.1 About",
        is_leaf=True,
        version_id=unexported_version.id,
        parent_id=collection_2.id,
    ).save()

    # sections

    # root
    #   - collection 1 (leaf)
    #       - section 1.1
    #   - collection 2
    #       - subcollection 2.1 (leaf)
    #           - section 2.1.1
    #           - section 2.1.2

    section_1_1 = m.Section(
        label="Dummy Section 1.1 Label",
        collection_id=collection_1.id,
        version_id=collection_1.version_id,
        user_id=user.id,
    ).save()

    section_2_1_1 = m.Section(
        label="Dummy Section 2.1.1 Label",
        collection_id=subcollection_2_1.id,
        version_id=unexported_version.id,
        user_id=user.id,
    ).save()

    section_2_1_2 = m.Section(
        label="Dummy Section 2.1.2 Label",
        collection_id=subcollection_2_1.id,
        version_id=unexported_version.id,
        user_id=user.id,
    ).save()

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

    interpretation_1 = m.Interpretation(
        text="Dummy Interpretation 1 About",
        section_id=section_1_1.id,
        user_id=user.id,
    ).save()

    interpretation_2 = m.Interpretation(
        text="Dummy Interpretation 2 About",
        section_id=section_2_1_1.id,
        user_id=user.id,
    ).save()

    interpretation_3 = m.Interpretation(
        text="Dummy Interpretation 3 About",
        section_id=section_2_1_2.id,
        user_id=user.id,
    ).save()

    m.Interpretation(
        text="Dummy Interpretation 4 About",
        section_id=section_2_1_2.id,
        user_id=user.id,
    ).save()

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

    comment_1 = m.Comment(
        text="Dummy Comment 1 Text",
        user_id=user_2.id,
        interpretation_id=interpretation_2.id,
    ).save()

    m.Comment(
        text="Dummy Comment 1.1 Text",
        user_id=user_3.id,
        parent_id=comment_1.id,
        interpretation_id=interpretation_2.id,
    ).save()

    m.Comment(
        text="Dummy Comment 1.2 Text",
        user_id=user_2.id,
        parent_id=comment_1.id,
        interpretation_id=interpretation_2.id,
    ).save()

    comment_2 = m.Comment(
        text="Dummy Comment 2 Text",
        user_id=user_4.id,
        interpretation_id=interpretation_2.id,
    ).save()

    comment_3 = m.Comment(
        text="Dummy Comment 3 Text",
        user_id=user.id,
        interpretation_id=interpretation_2.id,
    ).save()

    comment_3_1 = m.Comment(
        text="Dummy Comment 3.1 Text",
        user_id=user.id,
        parent_id=comment_3.id,
        interpretation_id=interpretation_2.id,
    ).save()

    comment_3_2 = m.Comment(
        text="Dummy Comment 3.2 Text",
        user_id=user.id,
        approved=True,
        parent_id=comment_3.id,
        interpretation_id=interpretation_2.id,
    ).save()

    comment_3_3 = m.Comment(
        text="Dummy Comment 3.3 Text",
        user_id=user.id,
        parent_id=comment_3.id,
        interpretation_id=interpretation_2.id,
    ).save()

    # - comment 3.1 (2 positive, 2 negative)
    # - comment 3.2 (1 negative)
    # - comment 3.3 (1 positive)
    m.CommentVote(comment_id=comment_3_1.id, user_id=user.id, positive=True).save()
    m.CommentVote(comment_id=comment_3_1.id, user_id=user_2.id, positive=True).save()
    m.CommentVote(comment_id=comment_3_1.id, user_id=user_3.id, positive=False).save()
    m.CommentVote(comment_id=comment_3_1.id, user_id=user_4.id, positive=False).save()
    m.CommentVote(comment_id=comment_3_2.id, user_id=user_2.id, positive=False).save()
    m.CommentVote(comment_id=comment_3_3.id, user_id=user_3.id, positive=True).save()

    # - interpretation 1 (2 positive, 1 negative)
    # - interpretation 2 (1 negative)
    # - interpretation 3 (1 positive)
    m.InterpretationVote(
        interpretation_id=interpretation_1.id, user_id=user.id, positive=True
    ).save()
    m.InterpretationVote(
        interpretation_id=interpretation_1.id, user_id=user_2.id, positive=True
    ).save()
    m.InterpretationVote(
        interpretation_id=interpretation_1.id, user_id=user_3.id, positive=False
    ).save()
    m.InterpretationVote(
        interpretation_id=interpretation_2.id, user_id=user_2.id, positive=False
    ).save()
    m.InterpretationVote(
        interpretation_id=interpretation_3.id, user_id=user_3.id, positive=True
    ).save()

    # tags
    tag_1 = m.Tag(name="Dummy Tag 1").save()
    tag_2 = m.Tag(name="Dummy Tag 2").save()
    tag_3 = m.Tag(name="Dummy Tag 3").save()

    # interpretation tags

    # - interpretation 1
    #   - tags: 1,
    # - interpretation 2
    #   - tags: 2, 3
    # - interpretation 3
    #   - tags: 1, 3
    m.InterpretationTag(interpretation_id=interpretation_1.id, tag_id=tag_1.id).save()
    m.InterpretationTag(interpretation_id=interpretation_2.id, tag_id=tag_2.id).save()
    m.InterpretationTag(interpretation_id=interpretation_2.id, tag_id=tag_3.id).save()
    m.InterpretationTag(interpretation_id=interpretation_3.id, tag_id=tag_1.id).save()
    m.InterpretationTag(interpretation_id=interpretation_3.id, tag_id=tag_3.id).save()

    # commen tags

    # - comment 1
    #   - tags: 1,
    # - comment 2
    #   - tags: 2, 3
    # - comment 3
    #   - tags: 1, 3
    m.CommentTags(comment_id=comment_1.id, tag_id=tag_1.id).save()
    m.CommentTags(comment_id=comment_2.id, tag_id=tag_2.id).save()
    m.CommentTags(comment_id=comment_2.id, tag_id=tag_3.id).save()
    m.CommentTags(comment_id=comment_3.id, tag_id=tag_1.id).save()
    m.CommentTags(comment_id=comment_3.id, tag_id=tag_3.id).save()
