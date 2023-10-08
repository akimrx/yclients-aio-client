class BaseHttpException(Exception):
    def __init__(self, method, url, params, response, result):
        self.method = method.upper()
        self.url = url
        self.params = params
        self.response = response
        self.result = result
        self.request_id = response.headers.get("x-request-id")
        super().__init__(
            f"Request-ID {self.request_id} failed with status code {self.response.status}. "
            f"HTTP Method: {self.method}, URL: {self.url}, Params: {self.params}. "
            f"Details: {self.result}"
        )


class HttpClientError(BaseHttpException):
    pass


class YclientsServerError(BaseHttpException):
    pass


class YclientsRateLimitted(BaseHttpException):
    pass


class MethodNotAllowed(Exception):
    pass


class UnparsableResponse(Exception):
    pass


class EmptyCompanyError(Exception):
    pass
