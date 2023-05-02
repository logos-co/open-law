import enum

from pydantic import BaseModel


class BreadCrumbType(enum.StrEnum):
    """Bread Crumb Type"""

    MyBookList = "MyBookList"
    AuthorBookList = "AuthorBookList"
    Collection = "Collection"
    Section = "Section"
    Interpretation = "Interpretation"


class BreadCrumb(BaseModel):
    """Bread Crumb for navigation"""

    label: str
    url: str
    type: BreadCrumbType
