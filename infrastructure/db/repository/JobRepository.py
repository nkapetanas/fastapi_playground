from sqlalchemy.orm import Session

from business.jobs import Job
from infrastructure.db.entities.JobEntity import JobEntity


def create_new_job(job: Job, db: Session, owner_id: int):
    job = JobEntity(**job.dict(), owner_id=owner_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def retrieve_job(id: int, db: Session):
    job = db.query(Job).filter(JobEntity.id == id).first()
    return job


def list_jobs(db: Session):
    jobs = db.query(Job).filter(JobEntity.is_active == True).all()
    return jobs


def update_job_by_id(id: int, job: JobEntity, db: Session, owner_id: int):
    existing_job = db.query(Job).filter(JobEntity.id == id)
    if not existing_job.first():
        return 0
    job.__dict__.update(owner_id=owner_id)
    existing_job.update(job.__dict__)
    db.commit()
    return 1


def delete_job_by_id(id: int, db: Session):
    existing_job = db.query(Job).filter(JobEntity.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1
