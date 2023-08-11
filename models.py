from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    employer = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    salary = models.CharField(max_length=30)

    creator = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.first().pk,null=False)

class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    university = models.CharField(max_length=100,null=True,blank=True,verbose_name='University Name')
    major = models.CharField(max_length=30,null=True,blank=True,verbose_name='Major')

    title = models.CharField(verbose_name='Title', max_length=100, null=True,blank=True)
    about = models.CharField(null=True,blank=True, max_length=1000,verbose_name='About')

    job1Title = models.CharField(verbose_name='Job 1 Title', max_length=100, null=True,blank=True)
    job1Employer = models.CharField(verbose_name='Job 1 Employer', max_length=100, null=True,blank=True)
    job1StartDate = models.CharField(verbose_name='Job 1 Start Date', max_length=100, null=True,blank=True)
    job1EndDate = models.CharField(verbose_name='Job 1 End Date', max_length=100, null=True,blank=True)
    job1Location = models.CharField(verbose_name='Job 1 Location', max_length=100, null=True,blank=True)
    job1Description = models.CharField(verbose_name='Job 1 Description', max_length=1000, null=True,blank=True)

    job2Title = models.CharField(verbose_name='Job 2 Title', max_length=100, null=True,blank=True)
    job2Employer = models.CharField(verbose_name='Job 2 Employer', max_length=100, null=True,blank=True)
    job2StartDate = models.CharField(verbose_name='Job 2 Start Date', max_length=100, null=True,blank=True)
    job2EndDate = models.CharField(verbose_name='Job 2 End Date', max_length=100, null=True,blank=True)
    job2Location = models.CharField(verbose_name='Job 2 Location', max_length=100, null=True,blank=True)
    job2Description = models.CharField(verbose_name='Job 2 Description', max_length=1000, null=True,blank=True)

    job3Title = models.CharField(verbose_name='Job 3 Title', max_length=100, null=True,blank=True)
    job3Employer = models.CharField(verbose_name='Job 3 Employer', max_length=100, null=True,blank=True)
    job3StartDate = models.CharField(verbose_name='Job 3 Start Date', max_length=100, null=True,blank=True)
    job3EndDate = models.CharField(verbose_name='Job 3 End Date', max_length=100, null=True,blank=True)
    job3Location = models.CharField(verbose_name='Job 3 Location', max_length=100, null=True,blank=True)
    job3Description = models.CharField(verbose_name='Job 3 Description', max_length=1000, null=True,blank=True)

    schoolName = models.CharField(verbose_name='School Name', max_length=100, null=True,blank=True)
    degree = models.CharField(verbose_name='Degree', max_length=100, null=True,blank=True)
    years = models.CharField(verbose_name='Years', max_length=100, null=True,blank=True)

    profileSet = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)

class userSetting(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.BooleanField(default=True)
    sms = models.BooleanField(default=True)
    targetedAds = models.BooleanField(default=True)
    english = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)

class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name = "from_user", on_delete = models.CASCADE)
    to_user = models.ForeignKey(User, related_name = "to_user", on_delete = models.CASCADE)

    accepted = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)

class Notification(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField(max_length=1000)

    isAboutJob = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)

class JobUserR(models.Model):
    graduationDate = models.DateField(verbose_name='Graduation Date',null=False,blank=False)
    startDate = models.DateField(verbose_name='Start Date',null=False,blank=False)
    msg = models.CharField(verbose_name='Why would you like the job?',max_length=100,null=True,blank=True)

    isApply = models.BooleanField(default=False) 
    isStarted = models.BooleanField(default=False) 

    jid = models.ForeignKey(Job, on_delete=models.CASCADE,null=False)
    uid = models.ForeignKey(User, on_delete=models.CASCADE,null=False)

# class Profile(models.Model):
#     title = models.CharField(max_length=30)
#     major = models.CharField(max_length=30)
#     university_name = models.CharField(max_length=30)
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
