import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import NewUserForm

@pytest.mark.django_db
def test_homeView(client):
    url = reverse('home:homepage')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_create():
    form_data = {'username': '123asdnv','email': 'testCaasd5@email.com', 'password1':'Vpcode123!','password2':'Vpcode123!'}
    form = NewUserForm(data=form_data)
    assert form.is_valid() == True
    form.save()
    assert User.objects.count() == 1

    form_data = {'username': 'test32ser','email': 'testC23eUser5@email.com', 'password1':'TESTdTTTTT','password2':'TESTdTTTTT'}
    form = NewUserForm(data=form_data)
    assert form.is_valid() == False
    
    form_data = {'username': 'asfvsd','emaial': 'testC23asdeUser5@email.com', 'password1':'123123123','password2':'123123123'}
    form = NewUserForm(data=form_data)
    assert form.is_valid() == False

@pytest.mark.django_db
def test_registerView(client):
    url = reverse('home:register')
    response = client.get(url)
    assert response.status_code == 200

    User.objects.create_user('testCaseUser', 'testCaseUser@email.com', 'password1')
    User.objects.create_user('testCaseUser2', 'testCaseUser2@email.com', 'password1')
    User.objects.create_user('testCaseUser3', 'testCaseUser3@email.com', 'password1')
    User.objects.create_user('testCaseUser4', 'testCaseUser4@email.com', 'password1')
    User.objects.create_user('testCaseUser5', 'testCaseUser5@email.com', 'password1')

    response = client.get(url)
    assert response.status_code == 302

