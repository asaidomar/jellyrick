from fastapi import APIRouter

router = APIRouter()


@router.get("/episode")
def episode_route() -> dict:
    """
    route to get episode data from rock and morty universe\n
    :return: json with episode data\n
    """
    response = {
    }

    return response
