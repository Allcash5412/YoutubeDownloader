from fastapi import HTTPException
from starlette import status


def get_exception_401_unauthorized_with_detail(detail: str) -> HTTPException:
    unauth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
    return unauth_exception