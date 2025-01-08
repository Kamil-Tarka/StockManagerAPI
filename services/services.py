from sqlalchemy.orm import Session

from models.entities import StockItem


class StockItemService:
    def __init__(self):
        pass

    def get_stock_item(self, db: Session, stock_item_id: int):
        stock_item = db.query(StockItem).filter(StockItem.id == stock_item_id).first()
        return stock_item


def get_stock_item_service() -> StockItemService:
    service = StockItemService()
    return service
