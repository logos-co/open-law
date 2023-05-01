from pydantic import BaseModel


class Breadcrumbs(BaseModel):
    """Breadcrumbs for navigation"""

    book_owner: str  # book owner name
    route_for_all_owners_books: str  # route for all book of this book owner
    current_user_is_owner: bool  # if current_user is owner of book
    book_name: str  # book label

    # How breadcrumbs must look like

    # if im not owner of a book
    # Home > Owner_name/All his books > This_book_name > Collection_name > Sub_collection_name > Section_name

    # if i owner
    # Home > My_books > This_book_name > Collection_name > Sub_collection_name > Section_name
