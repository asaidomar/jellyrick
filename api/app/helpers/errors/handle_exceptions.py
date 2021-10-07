from functools import wraps

from fastapi import HTTPException


# Decorator to handle exceptions in fastapi routes
def handle_exceptions(
    error_code: int or dict, error_message: dict, exception_types: tuple
):
    def handle_errors(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except exception_types as e:
                if type(e).__name__ in error_message.keys():
                    error_mes = error_message[type(e).__name__]
                    error_cod = error_code[type(e).__name__]
                else:
                    raise e
                print("ERROR:", type(e).__name__, ":", e)
                detail = {
                    "code": error_cod,
                    "message": f"{type(e).__name__}: {error_mes}",
                }
                raise HTTPException(status_code=error_cod, detail=detail)
            return result

        return wrapper

    return handle_errors
