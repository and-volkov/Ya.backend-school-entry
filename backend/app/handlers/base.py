from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from backend.app.models import ImportNode
from backend.db.schema import Node, ItemType


class NodeHandler:
    def __init__(self, db: Session):
        self.db = db

    def insert_or_update_nodes(self, input_nodes: ImportNode) -> None:
        node_items = input_nodes.items
        date = input_nodes.updateDate

        for item in node_items:
            item.date = date
            if item.type == 'FOLDER':
                item.type = ItemType.folder
            else:
                item.type = ItemType.file

        nodes = [n.dict() for n in node_items]
        stmt = insert(Node).values(nodes)
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_=dict(stmt.excluded)
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_node(self, node_id: str) -> Node:
        node = self.db.query(Node).filter(Node.id == node_id).cte(recursive=True)
        print(node)
        return node
