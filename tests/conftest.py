"""
Arquivo que configura os testes
"""

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        # Muda o banco de dados que será usado na hora dos testes para usar o
        # banco de dados em memória. Pois no get_session lá em database.py, foi
        # definido o banco de dados presente no arquivo .env que é o
        # banco de dados de produção.
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(model, time=datetime(2025, 9, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# Fixture que cria um usuário para aqueles testes que precisam
# da existência de um usuário
@pytest.fixture
def user(session: Session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
