from datetime import date
from typing import Optional

from business.jobs import JobBase


class JobJson(JobBase):
    title: str
    company: str
    company_url: Optional[str]
    location: str
    date_posted: date
    description: Optional[str]

    class Config():
        orm_mode = True
