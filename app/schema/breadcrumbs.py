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

    # How breadcrumbs must look like
    # Book List    > Book Name  > Top Level Collection > SubCollection > Section        > Interpretation

    # if im not owner of a book
    # John's books > Book Name  > Top Level Collection > SubCollection > Section        > Interpretation

    # if i owner
    # My Books     > Book Title > Part I               > Chapter X     > Paragraph 1.7  > By John
