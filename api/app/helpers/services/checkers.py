from fastapi import HTTPException


def check_item_not_found(user):
    if not user:
        raise HTTPException(status_code=404, detail="Item not found")
