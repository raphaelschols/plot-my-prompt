from typing import TypedDict
import uuid, traceback

def return_error(stage: str, code: str, exc: Exception = None, detail: str = None):
    if exc is not None:
        debug = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        message = f"{stage} failed: {exc}"
    else:
        debug = ""
        message = f"{stage} failed: {code.replace('_', ' ').title()}"
    return {
        "id": str(uuid.uuid4()),
        "stage": stage,
        "code": code,
        "message": message,
        "detail": detail,
        "debug": debug,
    }