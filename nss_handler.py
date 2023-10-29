import json
from enum import Enum
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler


class status(Enum):
    HTTP_200_SUCCESS = 200
    HTTP_201_CREATED = 201
    HTTP_204_SUCCESS_NO_BODY = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_404_NOT_FOUND = 404
    HTTP_405_UNSUPPORTED = 405
    HTTP_500_SERVER_ERROR = 500


class HandleRequests(BaseHTTPRequestHandler):
    def response(self, body, code):
        """Send HTTP response with body and status code

        Args:
            body (any): Data to send in response
            code (int): HTTP response code
        """
        self.set_response_code(body, code.value)
        self.wfile.write(body.encode())  # Where response to client happens

    def get_request_body(self):
        """Extract body from HTTP request

        Returns:
            string: JSON serialized request body
        """
        content_len = int(self.headers.get("content-length", 0))  # Returns integer
        request_body = self.rfile.read(content_len)  # string
        request_body = json.loads(request_body)  # converted the string to a dictionary
        return request_body  # returns a dictionary

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")
        resource = path_params[1]

        url_dictionary = {"requested_resource": resource, "query_params": {}, "pk": 0}

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            url_dictionary["query_params"] = query

        try:
            pk = int(path_params[2])
            url_dictionary["pk"] = pk
        except (IndexError, ValueError):
            pass

        return url_dictionary

    def set_response_code(self, body, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        if status_code == 405:
            self.send_header("Allow", ", ".join(body))
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()
