"""Rate-limited live scheme research, without accepting user-supplied URLs."""
from typing import Literal
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
from ..services import rate_limit, schemes
from ..services.tinyfish import TinyFishError

router = APIRouter(prefix='/api/schemes', tags=['farmer support'])
class SchemeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    state: str = Field(min_length=2, max_length=60, pattern=r'^[A-Za-z][A-Za-z &()-]+$')
    category: Literal['irrigation','solar','equipment','insurance','income']

@router.post('/search')
async def search_schemes(body: SchemeRequest, request: Request):
    rate_limit.limit_client(request, 'scheme-search', 6, 60)
    try:
        return await schemes.discover(body.state, body.category)
    except TinyFishError as exc:
        raise HTTPException(status_code=429 if exc.code == 'schemes_busy' else 503, detail=exc.code) from None
