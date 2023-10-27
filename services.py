def create_order(row):
    order = {
        "id": row["id"],
        "metalId": row["metalId"],
        "styleId": row["styleId"],
        "sizeId": row["sizeId"],
    }
    return order


def expand_metal(row):
    metal = {"id": row["metal_id"], "metal": row["metal"], "price": row["metal_price"]}
    return metal


def expand_style(row):
    style = {"id": row["style_id"], "style": row["style"], "price": row["style_price"]}
    return style


def expand_size(row):
    size = {"id": row["size_id"], "carets": row["carets"], "price": row["size_price"]}
    return size
