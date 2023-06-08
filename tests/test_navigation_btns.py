from flask.testing import FlaskClient

from tests.utils import (
    login,
    create_book,
    create_collection,
    create_sub_collection,
    create_section,
)


def test_approve_interpretation(client: FlaskClient):
    login(client)

    book = create_book(client)

    # --- TREE ---
    # main_col_1
    #   sub_col_1
    #       section_1
    #       section_2
    #       section_3
    #   sub_col_2
    #       section_4
    #   sub_col_3
    #      sub_col_4
    #          section_5
    # main_col_2
    #   sub_col_5
    #       sub_col_6
    #           sub_col_7
    #               sub_col_8
    #                   sub_col_9
    #                       section_6
    #                       section_7
    #           sub_col_10
    #                   section_8
    #                   section_9

    main_col_1, _ = create_collection(client, book.id)
    sub_col_1, _ = create_sub_collection(client, book.id, main_col_1.id)
    section_1, _ = create_section(client, book.id, sub_col_1.id)
    section_2, _ = create_section(client, book.id, sub_col_1.id)
    section_3, _ = create_section(client, book.id, sub_col_1.id)
    sub_col_2, _ = create_sub_collection(client, book.id, main_col_1.id)
    section_4, _ = create_section(client, book.id, sub_col_2.id)
    sub_col_3, _ = create_sub_collection(client, book.id, main_col_1.id)
    sub_col_4, _ = create_sub_collection(client, book.id, sub_col_3.id)
    section_5, _ = create_section(client, book.id, sub_col_4.id)
    main_col_2, _ = create_collection(client, book.id)
    sub_col_5, _ = create_sub_collection(client, book.id, main_col_2.id)
    sub_col_6, _ = create_sub_collection(client, book.id, sub_col_5.id)
    sub_col_7, _ = create_sub_collection(client, book.id, sub_col_6.id)
    sub_col_10, _ = create_sub_collection(client, book.id, sub_col_6.id)
    section_8, _ = create_section(client, book.id, sub_col_10.id)
    section_9, _ = create_section(client, book.id, sub_col_10.id)
    sub_col_8, _ = create_sub_collection(client, book.id, sub_col_7.id)
    sub_col_9, _ = create_sub_collection(client, book.id, sub_col_8.id)
    section_6, _ = create_section(client, book.id, sub_col_9.id)
    section_7, _ = create_section(client, book.id, sub_col_9.id)

    assert section_1.next_section == section_2
    assert section_2.next_section == section_3
    assert section_3.next_section == section_4
    assert section_4.next_section == section_5
    assert section_5.next_section == section_6
    assert section_6.next_section == section_7
    assert section_7.next_section == section_8
    assert section_8.next_section == section_9
    assert not section_9.next_section

    assert not section_1.previous_section
    assert section_2.previous_section == section_1
    assert section_3.previous_section == section_2
    assert section_4.previous_section == section_3
    assert section_5.previous_section == section_4
    assert section_6.previous_section == section_5
    assert section_7.previous_section == section_6
    assert section_8.previous_section == section_7
    assert section_9.previous_section == section_8
