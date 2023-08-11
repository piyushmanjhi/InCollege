from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, UserInfo, UserInfo, Friend_Request
from .models import JobUserR
import re

# Create your forms here.
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_password(value):
	if len(value) < 8 or len(value) > 12: 
		raise ValidationError( _('password needs to be between 8-12 chars'))
	if re.search('[a-z]', value) is None:
		raise ValidationError( _('Password needs lower case'))
	if re.search('[A-Z]', value) is None:
		raise ValidationError( _('Password needs upper case'))
	if re.search('[0-9]', value) is None:
		raise ValidationError( _('Password needs a number'))
	if re.search('[!@#$%^&*()`_=+]', value) is None:
		raise ValidationError( ('Password needs one of the following characters: !@#$%^&*()`_=+'))

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	university = forms.CharField(required=False)
	major = forms.CharField(required=False)
	
	password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
		validators=[validate_password],
    )

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "first_name","last_name", "university", "major")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		first_name = self.cleaned_data['first_name']
		last_name = self.cleaned_data['last_name']
		university = self.cleaned_data['university']
		major = self.cleaned_data['major']
		

		if commit:
			newUser = user.save()
			print(user)
			UserInfo.objects.get_or_create(firstName=first_name, lastName=last_name, university=university, major=major, user=user)

		return user

class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'employer', 'location', 'salary']

class LookupByName(forms.Form):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
class LookupByCollege(forms.Form):
	college = forms.CharField(required=True)
class LookupByMajor(forms.Form):
	major = forms.CharField(required=True)

class ChangeLangForm(forms.Form):
	isEnglish = forms.BooleanField(label="English",initial=True,required=False)

class ChangeSettingForm(forms.Form):
	email = forms.BooleanField(label="Email",initial=True,required=False)
	sms = forms.BooleanField(label="SMS",initial=True,required=False)
	targetedAds = forms.BooleanField(label="Targeted Ads",initial=True,required=False)


class ProfileCreationForm(forms.ModelForm):
	# def __init__(self, *args, **kwargs):
	# 		super(ProfileCreationForm, self).__init__(*args, **kwargs)
	# 		if True:
	# 			self.fields.pop('user')

	class Meta:
		model = UserInfo
		fields = ['title', 'major', 'university', 'about',
		'job1Title', 'job1Employer', 'job1StartDate', 'job1EndDate', 'job1Location', 'job1Description',
		'job2Title', 'job2Employer', 'job2StartDate', 'job2EndDate', 'job2Location', 'job2Description',
		'job3Title', 'job3Employer', 'job3StartDate', 'job3EndDate', 'job3Location', 'job3Description',
		'schoolName', 'degree', 'years',
		]
		widgets = {
            'about': forms.Textarea(),
            'job1Description': forms.Textarea(),
            'job2Description': forms.Textarea(),
            'job3Description': forms.Textarea(),
        }

	# title = forms.CharField(label='Title', max_length=100, required=False)
	# major = forms.CharField(label='Major', max_length=100, required=False)
	# university_name = forms.CharField(label='University Name', max_length=100)
	# about = forms.CharField(required=False, max_length=1000,label='About')

	# job1Title = forms.CharField(label='Job 1 Title', max_length=100, required=False)
	# job1Employer = forms.CharField(label='Job 1 Employer', max_length=100, required=False)
	# job1StartDate = forms.CharField(label='Job 1 Start Date', max_length=100, required=False)
	# job1EndDate = forms.CharField(label='Job 1 End Date', max_length=100, required=False)
	# job1Location = forms.CharField(label='Job 1 Location', max_length=100, required=False)
	# job1Description = forms.CharField(label='Job 1 Description', max_length=1000, required=False)

	# job2Title = forms.CharField(label='Job 2 Title', max_length=100, required=False)
	# job2Employer = forms.CharField(label='Job 2 Employer', max_length=100, required=False)
	# job2StartDate = forms.CharField(label='Job 2 Start Date', max_length=100, required=False)
	# job2EndDate = forms.CharField(label='Job 2 End Date', max_length=100, required=False)
	# job2Location = forms.CharField(label='Job 2 Location', max_length=100, required=False)
	# job2Description = forms.CharField(label='Job 2 Description', max_length=1000, required=False)

	# job3Title = forms.CharField(label='Job 3 Title', max_length=100, required=False)
	# job3Employer = forms.CharField(label='Job 3 Employer', max_length=100, required=False)
	# job3StartDate = forms.CharField(label='Job 3 Start Date', max_length=100, required=False)
	# job3EndDate = forms.CharField(label='Job 3 End Date', max_length=100, required=False)
	# job3Location = forms.CharField(label='Job 3 Location', max_length=100, required=False)
	# job3Description = forms.CharField(label='Job 3 Description', max_length=1000, required=False)

class ApplicationForm(forms.ModelForm):
	class Meta:
		model = JobUserR
		fields = ['graduationDate', 'startDate', 'msg'
		]
		widgets = {
            'graduationDate': forms.DateInput(format='%m/%d/%Y'),
            'startDate': forms.DateInput(format='%m/%d/%Y'),
            'msg': forms.Textarea(),
        }