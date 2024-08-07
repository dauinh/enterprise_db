from sqlalchemy.orm import Session

from app.api.models import Product


def get_product_attr(db: Session, product_id: int) -> dict:
    data = []
    product = db.get(Product, product_id)
    for assoc in product.attributes:
        attr = {'quantity': assoc.quantity}
        attr['color'] = assoc.attributes.color
        attr['size'] = assoc.attributes.size
        data.append(attr)

    return data