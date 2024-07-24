from fastapi import HTTPException
from starlette import status


def get_exception_400_bad_request_with_detail(detail: str) -> HTTPException:
    raise HTTPException(
        status_code=400,
        detail=detail
    )


def get_exception_401_unauthorized_with_detail(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )


def get_exception_404_not_found_with_detail(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )
