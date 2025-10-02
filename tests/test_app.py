from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Alice',
            'email': 'alice@gmail.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Alice',
        'email': 'alice@gmail.com',
        'id': 1,
    }


def test_create_existing_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'TestUser2',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    response = client.get('/users/')

    # Função que transforma o user que vem do banco, que vem com id, senha e
    # created_at em um userPublic, que é o que a rota get.users devolve
    user_schema = UserPublic.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_not_found_user(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'Bob',
            'email': 'bob@gmail.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_and_update_user_to_existing_username(client, user):
    client.post(
        '/users/',
        json={
            'username': 'Carlos',
            'email': 'carlos@gmail.com',
            'password': 'teste',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'carlos',
            'email': 'carlos@gmail.com',
            'password': 'ohmmm',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_inexistente(client):
    response = client.delete(
        '/users/999',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
