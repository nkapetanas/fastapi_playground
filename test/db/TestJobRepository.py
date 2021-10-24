from sqlalchemy.orm import Session

from business.jobs import Job
from infrastructure.db.repository.JobRepository import create_new_job, retrieve_job
from test.utils.users import create_random_owner


def test_retrieve_job_by_id(db_session: Session):
    title = "test title"
    company = "test comp"
    company_url = "testcomp.com"
    location = "USA,NY"
    description = "Foo bar"
    owner = create_random_owner(db=db_session)

    job = Job(title=title, company=company, company_url=company_url,
                     location=location, description=description)

    jobEntity = create_new_job(job=job, db=db_session, owner_id=owner.id)

    retrieved_job = retrieve_job(id=jobEntity.id, db=db_session)

    assert retrieved_job.id == jobEntity.id
    assert retrieved_job.title == "test title"
