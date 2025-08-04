from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/experiments",
    tags=["Experiments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Experiment)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    db_experiment = crud.get_experiment_by_name(db, name=experiment.name)
    if db_experiment:
        raise HTTPException(status_code=400, detail="Experiment already registered")
    return crud.create_experiment(db=db, experiment=experiment)

import uuid

@router.get("/{experiment_id}", response_model=schemas.Experiment)
def read_experiment(experiment_id: uuid.UUID, db: Session = Depends(get_db)):
    db_experiment = crud.get_experiment(db, experiment_id=experiment_id)
    if db_experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return db_experiment
