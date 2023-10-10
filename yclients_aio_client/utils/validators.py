import yclients_aio_client.constants as c
from yclients_aio_client.exceptions import EmptyCompanyError, MethodNotAllowed


def validate_company_id(main_company: str | None, arg_company: str | None) -> str:
    """Simple company ID validator."""
    if not any((main_company, arg_company)):
        raise EmptyCompanyError

    if arg_company is not None:
        return arg_company

    if main_company is not None:
        return main_company


def validate_method_is_allowed(method: str):
    if not isinstance(method, str) or method.lower() not in c.ALLOWED_HTTP_METHODS:
        raise MethodNotAllowed(f"Bad HTTP request method received. Allowed methods: {c.ALLOWED_HTTP_METHODS}")
