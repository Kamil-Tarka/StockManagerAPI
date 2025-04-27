"""
Pagination utility for handling paged results in the StockManagerAPI.
"""

from math import ceil

from models.models import PagedResult


def paginate(data, current_page, page_size, total_items):
    """
    Paginate the provided data and return a PagedResult object.

    Args:
        data (list): The list of items for the current page.
        current_page (int): The current page number (1-based).
        page_size (int): The number of items per page.
        total_items (int): The total number of items across all pages.

    Returns:
        PagedResult: An object containing paginated data and metadata.
    """
    return PagedResult(
        data=data,
        current_page=current_page,
        page_size=page_size,
        total_items=total_items,
        total_pages=int(ceil(total_items / page_size)),
    )
