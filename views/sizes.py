"""Size view module"""
import json
from nss_handler import status
from repository import db_get_all, db_get_single


class SizesView:
    """Style View Class"""

    def get(self, handler, query_params, pk):
        """Method for handling GET requests for /sizes
        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource
        Returns:
            handler response
        """

        sql = "SELECT s.id, s.carets, s.price FROM Sizes s"

        if pk != 0:
            sql += " WHERE s.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_sizes = json.dumps(dict(query_results))
        else:
            if "_sortBy" in query_params:
                sql += " ORDER BY s.price"
            query_results = db_get_all(sql)
            sizes = [dict(row) for row in query_results]
            serialized_sizes = json.dumps(sizes)

        return handler.response(serialized_sizes, status.HTTP_200_SUCCESS)
