from sqlalchemy.orm import Session

from backend.db.schema import Node, ItemType


def update_size_and_date(session: Session) -> None:
    """Update folders size before any commit."""
    stmt = (
        session.query(Node)
        .filter(Node.type == ItemType.folder)
        .order_by(Node.date.desc())
        .all()
    )
    for node in stmt:
        if node.children:
            node.size = sum(child.size for child in node.children)
            node.date = max(child.date for child in node.children)
