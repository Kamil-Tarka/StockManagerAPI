from math import ceil

from models.models import PagedResult


def paginate(data, current_page, page_size, total_items):
    return PagedResult(
        data=data,
        current_page=current_page,
        page_size=page_size,
        total_items=total_items,
        total_pages=int(ceil(total_items / page_size)),
    )
