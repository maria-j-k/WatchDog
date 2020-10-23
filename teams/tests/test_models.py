import pytest
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

from django.contrib.auth import authenticate
from django.urls import reverse

from teams.models import Dog, User

credits = {'username': 'john', 'password': 'smith'}
test_open_data = [('home', 200), ('teams:logout', 302)]
test_auth_data = [('home', credits, 200), ('teams:sign_in', credits, 200), ('teams:logout', credits, 302)]


@pytest.mark.django_db
@pytest.mark.parametrize('url, expected', test_open_data )
def test_open_views(client, url, expected):
    """Tests get request for views with no restrictions."""
    response = client.get(reverse(url))
    assert response.status_code == expected

@pytest.mark.django_db
def test_login_view(client):
    url = reverse('teams:login')
    response = client.get(url)
    response_post = client.post(reverse('teams:login'), {'username': 'john', 'password': 'smith'})
    assert response.status_code == 200
    assert response_post.status_code == 200

@pytest.mark.django_db
def test_protected_view(client, create_user):
    user = create_user(username='fantastic')
    client.force_login(user)
    url = reverse('training:profile', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_protected_view_fail(client, create_user):
    f_user = create_user()
    c_user = create_user(username='sogreat')
    client.force_login(c_user)
    url = reverse('training:profile', kwargs={'pk': f_user.pk})
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_protected_view_staff_may_access(client, create_staff_user):
    s_user = create_staff_user
    client.force_login(s_user)
    url = reverse('training:profile', kwargs={'pk': s_user.pk})
    response = client.get(url)
    assert response.status_code == 200

#@pytest.mark.django_db
#def test_send_invitation_view(client, create_staff_user):
#    s_user = create_staff_user
#    s_user.user_permissions.add('')
#    pass
