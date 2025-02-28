from fastapi import APIRouter, Depends
from ....services.visit_counter import VisitCounterService

router = APIRouter()
visit_counter_service = VisitCounterService()

def get_visit_counter_service():
    return visit_counter_service

@router.post("/visit/{page_id}")
def record_visit(
    page_id: str,
    counter_service: VisitCounterService = Depends(get_visit_counter_service)
):
    counter_service.increment_visit(page_id)
    return {"message": f"Visit recorded for {page_id}"}

@router.get("/visits/{page_id}")
def get_visits(
    page_id: str,
    counter_service: VisitCounterService = Depends(get_visit_counter_service)
):
    count = counter_service.get_visit_count(page_id)
    return {"visits": count}
