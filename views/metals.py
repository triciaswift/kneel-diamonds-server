"""Metal view module"""
import json
from nss_handler import status
from repository import db_get_all, db_get_single


class MetalsView:
    """Metal View Class"""

    def get(self, handler, query_params, pk):
        """Method for handling GET requests for /metals
        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource
        Returns:
            response
        """

        sql = "SELECT m.id, m.metal, m.price FROM Metals m"

        if pk != 0:
            sql += " WHERE m.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_metals = json.dumps(dict(query_results))
        else:
            if "_sortBy" in query_params:
                sql += " ORDER BY m.price"
            query_results = db_get_all(sql)
            metals = [dict(row) for row in query_results]
            serialized_metals = json.dumps(metals)

        return handler.response(serialized_metals, status.HTTP_200_SUCCESS)
