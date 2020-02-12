from http import HTTPStatus

from starlette.exceptions import HTTPException


class Unauthorized(HTTPException):
    """No permission -- see authorization schemes"""

    def __init__(self, detail: str = None):
        HTTPException.__init__(
            self,
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail=detail or HTTPStatus.UNAUTHORIZED.description,
        )


class Forbidden(HTTPException):
    """Request forbidden -- authorization will not help"""

    def __init__(self, detail: str = None):
        HTTPException.__init__(
            self,
            status_code=HTTPStatus.FORBIDDEN.value,
            detail=detail or HTTPStatus.FORBIDDEN.description,
        )
