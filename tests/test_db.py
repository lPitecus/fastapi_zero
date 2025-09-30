from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    # Define qual usuário será criado no banco de dados,
    # baseado na estrutura do User definida no models.py
    new_user = User(username='test', email='test@test', password='test')

    # Declara que quer adicionar esse usuário no banco de dados
    session.add(new_user)

    # De fato insere esse usuário no banco de dados
    session.commit()

    # Faz uma busca do usuário criado no banco
    user = session.scalar(select(User).where(User.username == 'test'))
    assert user.username == 'test'
