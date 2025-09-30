from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    # Define qual usuário será criado no banco de dados,
    # baseado na estrutura do User definida no models.py
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='test')

        # Declara que quer adicionar esse usuário no banco de dados
        session.add(new_user)

        # De fato insere esse usuário no banco de dados
        session.commit()

        # Faz uma busca do usuário criado no banco
        user = session.scalar(select(User).where(User.username == 'test'))
    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'test',
        'created_at': time,
    }
