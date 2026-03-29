import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from main import app
from database import get_session


@pytest.fixture
def session():
       engine = create_engine("sqlite:///:memory:")
       SQLModel.metadata.create_all(engine)
       with Session(engine) as s:
           yield s
  
  
@pytest.fixture
def client(session):
       app.dependency_overrides[get_session] = lambda: session
       yield TestClient(app)
       app.dependency_overrides.clear()