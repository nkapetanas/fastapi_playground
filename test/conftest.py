import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py

from infrastructure.db.base_class import Base
from infrastructure.db.session import get_db
from api.base import api_router

"""
We are creating a new Fastapi instance, app, and a brand new database. 
This is an SQLite database and we don't need to do anything because python will create a file - test_db.db
We are doing this because we don't want to mess up our original database with test data.
The good thing is we have not hardcoded the database to be used in the routes. 
We are making use of a dependency named 'get_db' to provide a database session.
In our unit tests, we will be overriding this dependency and provide our test database instead. 
This concept is known as dependency injection.
There is a rule that each test should be independent. So, we are resetting/rollbacking the changes in the db tables and even creating a new database for each test! 
Notice we have made 'client' as a function test fixture. So, by using this client we would be able to rollback things and keep our tests isolated and independent.
For each function in this tests folder, we would clean our database after running it. Let's try our work : Type the below code in tests > restservices > TestUserRest.py
"""


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
