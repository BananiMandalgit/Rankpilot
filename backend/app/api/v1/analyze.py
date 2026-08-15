from fastapi import APIRouter, HTTPException

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.analysis import AnalysisService

router = APIRouter(prefix='/analyze', tags=['analyze'])

service = AnalysisService()


@router.post('', response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    # Route handler kept thin: validate via Pydantic, delegate to service
    try:
        result = service.analyze(str(request.url))
    except ValueError:
        raise HTTPException(status_code=422, detail='invalid url')

    return result
