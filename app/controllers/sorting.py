from sqlalchemy import text
from app.logger import log
from app.controllers import create_pagination


def sort_by(query, sort: str):
    match sort:
        case "favorited":
            query = query.order_by(text("stars_count DESC"))
        case "upvoted":
            query = query.order_by(text("score DESC"))
        case "recent":
            query = query.order_by(text("created_at DESC"))
        case "commented":
            query = query.order_by(text("comments_count DESC"))
        case "interpretations":
            query = query.order_by(text("interpretations_count DESC"))
        case _:
            query = query.order_by(text("created_at DESC"))

    pagination = create_pagination(total=query.count())
    log(log.INFO, "Returns data for front end")

    query = query.paginate(page=pagination.page, per_page=pagination.per_page)
    query.items = [item[0] for item in query.items]
    return pagination, query
