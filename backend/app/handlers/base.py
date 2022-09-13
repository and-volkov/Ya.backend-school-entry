import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from backend.app.models import ImportNode
from backend.db.schema import Node, ItemType


class NodeHandler:
    def __init__(self, db: Session):
        self.db = db

    def get_node(self, node_id) -> Node:
        return self.db.query(Node).filter(Node.id == node_id).first()

    def delete_node(self, node_id) -> None:
        self.db.query(Node).filter(Node.id == node_id).delete()
        self.db.commit()

    @classmethod
    def process_node(cls, input_nodes: ImportNode) -> list[Node]:
        node_items = input_nodes.items
        date = input_nodes.updateDate

        for item in node_items:
            item.date = date
            if item.type == 'FOLDER':
                item.type = ItemType.folder
                item.size = 0
            else:
                item.type = ItemType.file
        return node_items

    def insert_or_update(self, values: dict | list[dict]) -> None:
        stmt = insert(Node).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'], set_=dict(stmt.excluded)
        )
        self.db.execute(stmt)
        self.db.commit()

    def insert_or_update_nodes(self, input_nodes: ImportNode) -> None:
        node_items = self.process_node(input_nodes)

        nodes = [node.dict() for node in node_items]
        self.insert_or_update(nodes)

    def get_node_updates(self, date: datetime):
        delta = datetime.timedelta(hours=24)
        start_date = date - delta
        return (
            self.db.query(Node)
            .filter(and_(
                Node.date.between(start_date, date),
                Node.type == ItemType.file)
            )
            .all()
        )
