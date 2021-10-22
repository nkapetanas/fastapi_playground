from typing import List

from api.v1.jobs.JobJson import JobJson
from api.v1.route_login import get_current_user_from_token
from infrastructure.db.entities.users import User
from infrastructure.db.repository.jobRepository import (create_new_job, retreive_job, list_jobs, update_job_by_id,
                                                        delete_job_by_id)
from infrastructure.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from business.jobs import Job

router = APIRouter()


@router.post("/create-job", response_model=JobJson)
def create_job(job: Job, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user_from_token)):
    owner_id = current_user.id
    job = create_new_job(job=job, db=db, owner_id=owner_id)
    return job


@router.get("/get/{id}", response_model=JobJson)
def retreive_job_by_id(id: int, db: Session = Depends(get_db)):
    job = retreive_job(id=id, db=db)
    print(job)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} does not exist")
    return job


@router.get("/all", response_model=List[JobJson])
def retrieve_all_jobs(db: Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs


@router.put("/update/{id}")
def update_job(id: int, job: Job, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user_from_token)):
    owner_id = current_user.id
    job_retrieved = retreive_job(id=id, db=db)
    if not job_retrieved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} does not exist")
    if job_retrieved.owner_id == current_user.id or current_user.is_superuser:
        message = update_job_by_id(id=id, job=job, db=db, owner_id=owner_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not authorized to update.")
    return {"detail": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_job(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    job = retreive_job(id=id, db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} does not exist")
    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Job Successfully deleted"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not permitted!!")
