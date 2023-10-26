"""Order view module"""
import json
from nss_handler import status
from repository import db_get_all, db_get_single, db_create
from datetime import date


class OrdersView:
    def get(self, handler, pk):
        """Method for handling GET requests for /orders
        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource
        Returns:
            handler response
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
