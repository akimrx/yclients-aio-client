from yclients_aio_client.exceptions import EmptyCompanyError


def validate_company_id(main_company: str | None, arg_company: str | None) -> str:
    """Simple company ID validator."""
    if not any((main_company, arg_company)):
        raise EmptyCompanyError

    if arg_company is not None:
        return arg_company

    if main_company is not None:
        return main_company
