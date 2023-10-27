"""Order view module"""
import json
from nss_handler import status
from repository import db_get_all, db_get_single, db_create, db_delete
from services import create_order, expand_metal, expand_style, expand_size


class OrdersView:
    def get(self, handler, query_params, pk):
        """Method for handling GET requests for /orders
        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource
        Returns:
            JSON string & integer
        """

        sql = "SELECT o.id, o.metalId, o.styleId, o.sizeId, o.timestamp FROM Orders o"

        if pk != 0:
            sql += " WHERE o.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_orders = json.dumps(dict(query_results))
        else:
            query_results = db_get_all(sql)
            orders = [dict(row) for row in query_results]
            serialized_orders = json.dumps(orders)

        return handler.response(serialized_orders, status.HTTP_200_SUCCESS)

    def create(self, handler, order_data):
        sql = """
        INSERT INTO Orders (metalId, styleId, sizeId)
        VALUES (?, ?, ?)
        """
        last_row = db_create(
            sql, (order_data["metalId"], order_data["styleId"], order_data["sizeId"])
        )

        if last_row is not None:
            order = {
                "id": last_row["id"],
                "metalId": order_data["metalId"],
                "styleId": order_data["styleId"],
                "sizeId": order_data["sizeId"],
                "timestamp": last_row["timestamp"],
            }
            return handler.response(json.dumps(order), status.HTTP_201_CREATED)
        else:
            return handler.response("", status.HTTP_404_NOT_FOUND)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Orders WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_BODY)
        else:
            return handler.response("", status.HTTP_404_NOT_FOUND)

    def expand(self, handler, query_params, pk):
        sql = "SELECT o.id, o.metalId, o.styleId, o.sizeId, m.id metal_id, m.metal, m.price metal_price, s.id style_id, s.style, s.price style_price, z.id size_id, z.carets,z.price size_price FROM Orders o JOIN Metals m ON o.metalId = metal_id JOIN Styles s ON o.metalId = style_id JOIN Sizes z ON o.metalId = size_id"
        if pk != 0:
            sql += " WHERE o.id = ?"
            query_results = db_get_single(sql, pk)
            order = create_order(query_results)

            if "metal" in query_params["expand"]:
                selected_metal = expand_metal(query_results)
                order["metal"] = selected_metal
            if "style" in query_params["expand"]:
                selected_style = expand_style(query_results)
                order["style"] = selected_style
            if "size" in query_params["expand"]:
                selected_size = expand_size(query_results)
                order["size"] = selected_size

            serialized_hauler = json.dumps(order)
            return handler.response(serialized_hauler, status.HTTP_200_SUCCESS)

        else:
            query_results = db_get_all(sql)
            orders = []
            for row in query_results:
                order = create_order(row)

                if "metal" in query_params["expand"]:
                    selected_metal = expand_metal(row)
                    order["metal"] = selected_metal
                if "style" in query_params["expand"]:
                    selected_style = expand_style(row)
                    order["style"] = selected_style
                if "size" in query_params["expand"]:
                    selected_size = expand_size(row)
                    order["size"] = selected_size

                orders.append(order)

            serialized_orders = json.dumps(orders)

            return handler.response(serialized_orders, status.HTTP_200_SUCCESS)
