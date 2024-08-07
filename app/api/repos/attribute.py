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


def is_attr_quantities_equal_total(db: Session, product_id: int) -> bool:
    product = db.get(Product, product_id)
    total = product.total_quantity
    count = 0
    for assoc in product.attributes:
        count += assoc.quantity
    return total == count