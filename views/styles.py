"""Style view module"""
import json
from nss_handler import status
from repository import db_get_all, db_get_single


class StylesView:
    """Style View Class"""

    def get(self, handler, pk):
        """Method for handling GET requests for /styles
        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource
        Returns:
            handler response
        """

        sql = "SELECT s.id, s.style, s.price FROM Styles s"

        if pk != 0:
            sql += " WHERE s.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_styles = json.dumps(dict(query_results))
        else:
            query_results = db_get_all(sql)
            styles = [dict(row) for row in query_results]
            serialized_styles = json.dumps(styles)

        return handler.response(serialized_styles, status.HTTP_200_SUCCESS)
