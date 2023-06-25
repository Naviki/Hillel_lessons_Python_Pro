import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_create_card(client):

    data = {
        'card_number': '1234567890123456',
        'expiration_date': '12/25',
        'cvv': '123',
        'issue_date': '2023-06-25',
        'owner_id': '00000000-0000-0000-0000-000000000000',
        'status': 'active'
    }
    # When
    response = client.post('/cards', json=data)
    # Then
    assert response.status_code == 200
    assert response.json['message'] == 'Card created successfully'

def test_get_card(client):
    # When
    response = client.get('/cards/1234567890123456')
    # Then
    assert response.status_code == 200
    assert response.json['card_number'] == '1234567890123456'

    # When
    response = client.get('/cards/9999999999999999')
    # Then
    assert response.status_code == 200
    assert response.json['message'] == 'Card not found'