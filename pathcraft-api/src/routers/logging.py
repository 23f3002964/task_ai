from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/logging",
    tags=["Logging and Metrics"],
    responses={404: {"description": "Not found"}},
)

@router.post("/metrics", response_model=schemas.Metric)
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    return crud.create_metric(db=db, metric=metric)

@router.post("/logs", response_model=schemas.Log)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db=db, log=log)
