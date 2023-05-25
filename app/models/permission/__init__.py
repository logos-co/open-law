# flake8: noqa F401
from .access_group import AccessGroup
from .permission import Permission
from .user_access_groups import UserAccessGroups
from .permission_access_groups import PermissionAccessGroups
from .book_access_groups import BookAccessGroups
from .collection_access_groups import CollectionAccessGroups
from .section_access_groups import SectionAccessGroups
from .interpretation_access_groups import InterpretationAccessGroups

# access groups
#   moderators(by default empty) -> root collection -> CRUD Interpretation, Comment
#   editors(by default empty) -> root collection -> CRUD Collection, Section
#
#   on create collection/section -> inherit parent's access groups
#

# add to collection, sections, ...
#  - access_groups -> access group table

# access group:
#   - name
#   - users many-to-many = []
#   - permissions many-to-many = []

# permission:
#   - access [Enum(CRUD)]
#   - entity [Enum(collection, sections, ...)]
#   - access_group -> access group table


# Book
# Version:
#   Root Collection
#       Collection A
#           Section
#           Section
#       Collection B
#           SubCollection B.1
#               Section
#               Section
#           SubCollection B.2
#               Section
#               Section

# If the user has CRUD access to Collection B it means that
# it has access to all nested entities(SubCollection B.1/B.2, Sections)


# 1) Create moderator_AG and editor_AG on book create
# 2) Inherit parent's access groups

# TODO many to many
# book -> access_group
# collections -> access_group
# section -> access_group
# interpretation -> access_group