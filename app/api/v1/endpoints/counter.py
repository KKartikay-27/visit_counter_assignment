from fastapi import APIRouter, HTTPException, Depends
from ....services.visit_counter import VisitCounterService
from ....schemas.counter import VisitCount

router = APIRouter()

# ✅ Create a single instance of VisitCounterService
visit_counter_service = VisitCounterService()

def get_visit_counter_service():
    """Always return the same instance"""
    return visit_counter_service

@router.post("/visit/{page_id}")
def record_visit(
    page_id: str,
    counter_service: VisitCounterService = Depends(get_visit_counter_service)
):
    """Record a visit for a website"""
    try:
        counter_service.increment_visit(page_id)
        return {"status": "success", "message": f"Visit recorded for page {page_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visits/{page_id}", response_model=VisitCount)
def get_visits(
    page_id: str,
    counter_service: VisitCounterService = Depends(get_visit_counter_service)
):
    """Get visit count for a website"""
    try:
        count = counter_service.get_visit_count(page_id)
        return VisitCount(visits=count, served_via="redis")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
