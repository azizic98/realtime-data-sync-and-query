from fastapi import HTTPException,status
from fastapi import APIRouter,Query
from app import (connections,
                utils,
                helpers,
                operations,
                schemas)
from typing import List


router = APIRouter()


@router.get("/health-check",status_code=status.HTTP_200_OK)
async def health_check():
    return {"message": "Hello World"}

@router.post("/check_duplicates")
def check_duplicates(data: schemas.DuplicateIn):
    table = data.table
    field = data.field
    value = utils.escape_special_characters(data.value)


    if table == 'tbl_reporters':

        results = operations.get_duplicates_from_redis(field, value, schemas.ReporterIndexSchema.name)
        return helpers.check_duplicates_reporters(results, field)
    
    elif table == 'tbl_outlets':

        results = operations.get_duplicates_from_redis(field, value, schemas.OutletIndexSchema.name)
        return helpers.check_duplicates_outlets(results, field)
    
    else:
        raise HTTPException(status_code=400, detail="Invalid table specified")
    

@router.get("/autocomplete", response_model=List[str])
async def autocomplete(query: str = Query(..., min_length=1),limit: int = 5):
    # Fetch suggestions from Redis
    suggestions = connections.redis_client.execute_command('FT.SUGGET', 'name_autocomplete', query,'MAX',limit)
    return [] if not suggestions else suggestions

