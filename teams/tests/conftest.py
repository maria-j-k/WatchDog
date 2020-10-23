import pytest

from teams.models import User, Dog


@pytest.fixture
def test_password():
    return 'strongpasswordfortests'


@pytest.fixture
def create_email(name):
    return f'{name}@test.pl'


@pytest.fixture
def create_user(db, test_password):
    def make_user(**kwargs):
        data = {
            'username': 'John',
            'password': test_password,
            'email': create_email,
            'zip_code': '00-444',
            'country': 'pl',
            'lat': 52,
            'lon': 21,
            'location': 'Warszawa'
    }
        dog_data = {
            'dogs_name': 'Burek',
            'dogs_birthday': '2020-11-11',
            'dogs_bread': 'springer spaniel',
            'team_description': 'test description'
        }
        for key in data:
            if not key in kwargs:
                kwargs[key] = data[key]
        user = User.objects.create(**kwargs)
        dog = Dog.objects.create(user=user, **dog_data)
        return user
    return make_user

@pytest.fixture
def create_staff_user(db, create_user):
    user = create_user()
    user.is_staff = True
    user.save()
    return user
