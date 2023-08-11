import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import NewUserForm, NewJobForm
from .models import Job

## First get all jobs
## Now add a new job
## Get all jobs again and verify new job is in there

@pytest.mark.django_db
def test_new_job_creation(client):
    form_data = {'title': 'Test Job', 'description': 'Test Description', 'employer': 'Test Employer', 'location': 'Test Location', 'salary': 'Test Salary'}
    form = NewJobForm(data=form_data)
    assert form.is_valid() == True
    form.save()
    assert len(Job.objects.all()) == 2
