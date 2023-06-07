from app import models as m


def get_next_section(collection: m.Collection):
    if collection.active_sections:
        return collection.active_sections[0]

    # find on current level in next by order collections
    for child in collection.active_children:
        if section := get_next_section(child):
            return section


def recursive_move_down(collection: m.Collection):
    parent: m.Collection = collection.parent
    current: m.Collection = collection
    while True:
        if len(parent.active_children) > current.position + 1:
            index = parent.active_children.index(current) + 1
            for child in parent.active_children[index:]:
                if section := get_next_section(child):
                    return section

        if current.is_root or not current.parent:
            return None

        current = parent
        parent = parent.parent


def get_prev_section(collection: m.Collection):
    if collection.active_sections:
        return collection.active_sections[-1]

    # find on current level in next by order collections
    for child in collection.active_children[::-1]:
        if section := get_prev_section(child):
            return section


def recursive_move_up(collection: m.Collection):
    parent: m.Collection = collection.parent
    current: m.Collection = collection
    while True:
        index = parent.active_children.index(current)
        if parent.active_children[:index]:
            for child in parent.active_children[:index][::-1]:
                if section := get_prev_section(child):
                    return section

        if current.is_root or not current.parent:
            return None

        current = parent
        parent = parent.parent
