# flake8: noqa F401
from .auth import LoginForm
from .user import UserForm, NewUserForm
from .book import CreateBookForm, EditBookForm
from .contributor import (
    AddContributorForm,
    DeleteContributorForm,
    EditContributorRoleForm,
)
from .collection import CreateCollectionForm, EditCollectionForm
from .section import CreateSectionForm, EditSectionForm
from .interpretation import CreateInterpretationForm, EditInterpretationForm
