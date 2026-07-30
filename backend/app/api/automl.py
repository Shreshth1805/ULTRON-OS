from fastapi import APIRouter, HTTPException

from app.schemas.automl import (
    AutoMLRequest,
    AutoMLResponse
)

from app.tools.registry import get_agent


router = APIRouter(
    prefix="/automl",
    tags=["AutoML"]
)


@router.post(
    "/train",
    response_model=AutoMLResponse
)
def train_model(
    request: AutoMLRequest
):

    agent = get_agent(
        "automl_agent"
    )

    if agent is None:

        raise HTTPException(
            status_code=500,
            detail="AutoML agent is not available."
        )

    try:

        result = agent.train(
            filename=request.filename,
            target_column=request.target_column
        )

        return {
            "status": "success",
            "message": "AutoML training completed.",
            "results": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )