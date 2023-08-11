from django.shortcuts import  render, redirect
from .forms import NewUserForm, NewJobForm, LookupByName, ChangeLangForm, LookupByCollege, LookupByMajor
from .forms import ChangeSettingForm, ProfileCreationForm, ApplicationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Job, userSetting, UserInfo, Friend_Request
from .models import Notification, JobUserR
from django.http import HttpResponse
from django.db.models import Q
import datetime

# Create your views here.
def homepage(request):
	if request.user.is_authenticated:
		friendRequest = Friend_Request.objects.filter(to_user=request.user).filter(valid=True)
		notis = Notification.objects.filter(user=request.user)
	else:
		friendRequest = None
		notis = None
	return render(request=request, template_name='home/home.html', context={
		'friendRequest':friendRequest,
		'notis': notis,
	})

def job_search(request):
	jobs = Job.objects.exclude(creator=request.user)
	notis = Notification.objects.filter(user=request.user).filter(isAboutJob=True)

	for noti in notis:
		noti.delete()

	return render(request, 'home/jobsearch.html', context={'jobs': jobs,
						"notis": notis, })
def makeajob(request):
	if len(Job.objects.all()) >= 10:
		messages.error(request, f"Sorry, we have reached our max jobs counts, please check back later.")
		return redirect("home:jobsearch")
	if request.method == 'POST':
		form = NewJobForm(request.POST)
		if form.is_valid():
			newJob = form.save(commit=False)
			newJob.creator = request.user
			newJob.save()
			jobs = Job.objects.all()
			messages.success(request, f"Job created")
			return redirect('home:jobs')
	else:
		form = NewJobForm()
	return render(request, 'home/makeajob.html', {'form': form})

def find_someone(request):
	curU = User.objects.get(pk=request.user.pk) 
	form = LookupByName()
	form2 = LookupByCollege()
	form3 = LookupByMajor()
	user = None
	if request.method == "POST":
		print(request.POST)
		if "name-bnt" in request.POST:
			form = LookupByName(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data.get('first_name')
				last_name = form.cleaned_data.get('last_name')
				
				user = User.objects.filter(first_name=first_name).filter(last_name=last_name)
				print(user)
				if len(user) >= 1:
					messages.success(request, "They are a part of the InCollege system.")
				else:
					messages.error(request,"They are not yet a part of the InCollege system yet.")

		if "college-bnt" in request.POST:
			form2 = LookupByCollege(request.POST)
			if form2.is_valid():
				college = form2.cleaned_data.get('college')
				
				user = UserInfo.objects.filter(university=college)
				linkBack = []
				for i in user:
					linkBack.append(i.user)
				user = linkBack
				if len(user) >= 1:
					messages.success(request, "They are a part of the InCollege system.")
				else:
					messages.error(request,"They are not yet a part of the InCollege system yet.")

		if "major-bnt" in request.POST:
			form3 = LookupByMajor(request.POST)
			if form3.is_valid():
				major = form3.cleaned_data.get('major')
				
				user = UserInfo.objects.filter(major=major)
				linkBack = []
				for i in user:
					linkBack.append(i.user)
				user = linkBack
				if len(user) >= 1:
					messages.success(request, "They are a part of the InCollege system.")
				else:
					messages.error(request,"They are not yet a part of the InCollege system yet.")

	return render(request=request, template_name='home/findsomeone.html',context={'form':form,'form2':form2,'form3':form3,'users':user})

def skill(request):
	return render(request=request, template_name='home/skill.html')

def underConstruction(request):
	return render(request=request, template_name='home/under_construction.html')

def register_request(request):
	form = NewUserForm()
	if len(User.objects.all()) >= 10 :
		messages.error(request, "Sorry, we have reached max users, check back later!" )
		return redirect("home:homepage")
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="home/register.html", context={"register_form":form})

def login_request(request):
	form = AuthenticationForm()
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	return render(request=request, template_name="home/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home:homepage")

def video_display(request):
	return render(request=request, template_name='home/video_display.html')


def general(request):
	return render(request=request, template_name='home/general.html')

def Browse_InCollege(request):
	return render(request=request, template_name='home/Browse_InCollege.html')

def buisness_solutions(request):
	return render(request=request, template_name='home/buisness_solutions.html')

def Directories(request):
	return render(request=request, template_name='home/Directories.html')

def copyright_notice(request):
	return render(request=request, template_name='home/copyright_notice.html')

def About(request):
	return render(request=request, template_name='home/About.html')

def Accessibility(request):
	return render(request=request, template_name='home/Accessibility.html')

def User_Agreement(request):
	return render(request=request, template_name='home/User_Agreement.html')

def Privacy_Policy(request):
	return render(request=request, template_name='home/Privacy_Policy.html')

def Cookie_Policy(request):
	return render( request = request, template_name = "home/Cookie_policy.html")

def Copyright_Policy(request):
	return render(request=request, template_name='home/CopyRight_Policy.html')

def Brand_Policy(request):
	return render(request=request, template_name='home/Brand_Policy.html')

def Guest_Controls(request):
	form = ChangeSettingForm()
	if request.method == "POST":
		print(request.POST)
		form = ChangeSettingForm(request.POST)
		if form.is_valid():
			usrSet, _ = userSetting.objects.get_or_create(user=request.user)
			usrSet.email = form.cleaned_data.get('email')
			usrSet.sms = form.cleaned_data.get('sms')
			usrSet.targetedAds = form.cleaned_data.get('targetedAds')
			usrSet.save()

			messages.success(request,"Updated")
		else:
			messages.error(request,"Fail to update.")
		return redirect("home:homepage")
	return render(request=request, template_name='home/Guest_Controls.html',context={"form":form})

def Languages(request):
	form = ChangeLangForm()
	if request.method == "POST":
		print(request.POST)
		form = ChangeLangForm(request.POST)
		if form.is_valid():
			usrSet, _ = userSetting.objects.get_or_create(user=request.user)
			usrSet.english = form.cleaned_data.get('isEnglish')
			usrSet.save()
			messages.success(request,"Updated")
		else:
			messages.error(request,"Fail to update.")
			return redirect("home:homepage")
	return render(request=request, template_name='home/Languages.html',context={"form":form})

def Help_Center(request):
	return render(request=request, template_name='home/Help_Center.html')

def Press(request):
	return render(request=request, template_name='home/Press.html')

def Blog(request):
	return render(request=request, template_name='home/Blog.html')

def Careers(request):
	return render(request=request, template_name='home/Careers.html')

def Developers(request):
	return render(request=request, template_name='home/Developers.html')

def NetworkView(request):
	friends = Friend_Request.objects.filter(accepted=True).filter(Q(to_user=request.user) | Q(from_user=request.user))
	print(friends)
	return render(request=request, template_name='home/networks.html',context={'friends':friends})


def send_friend_request_view(request,pk=None):
	from_user = request.user
	to_user = User.objects.get(pk=pk)
	obj = Friend_Request.objects.get_or_create(from_user=from_user,to_user=to_user)
	messages.success(request,"Request sent")
	return redirect("home:findsomeone")
def accept_friend_request_view(request,pk=None):
	friendRequest = Friend_Request.objects.get(pk=pk)
	friendRequest.accepted = True
	friendRequest.valid = False
	friendRequest.save()
	messages.success(request,"You guys are now frineds")
	return redirect("home:homepage")
def reject_friend_request_view(request,pk=None):
	friendRequest = Friend_Request.objects.get(pk=pk)
	friendRequest.accepted = False
	friendRequest.valid = False
	friendRequest.save()
	messages.success(request,"Request Rejected")
	return redirect("home:homepage")
def remove_friend_request_view(request,pk=None):
	Friend_Request.objects.get(pk=pk).delete()
	messages.success(request,"Friend Deleted!")
	return redirect("home:Networks")


def edit_Profile(request):
	form = ProfileCreationForm()
	curUserinfo, _ = UserInfo.objects.get_or_create(user=request.user)
	form = ProfileCreationForm(instance=curUserinfo)

	if request.method == "POST":
		form = ProfileCreationForm(request.POST,instance=curUserinfo)
		if form.is_valid():
			newP=form.save(commit=False)
			newP.profileSet=True
			if newP.major is not None:
				newP.major = newP.major.title()
			if newP.university is not None:
				newP.university = newP.university.title()
			if newP.schoolName is not None:
				newP.schoolName = newP.schoolName.title()

			newP.save()
			messages.success(request,"Profile Updated")
			return redirect("home:homepage")
		else:
			messages.error(request,"Profile Fail to Update")
	return render(request=request, template_name="home/editProfile.html", context={'form':form})


def Profile_view(request,pk=None):
	target = User.objects.get(pk=pk)
	
	userConnections = Friend_Request.objects.filter(accepted=True).filter((Q(to_user=request.user) & Q(from_user=target))|(Q(from_user=request.user) & Q(to_user=target)))
	profile=None
	isFriend=False
	hasProfile=False
	if userConnections.count() != 0:
		isFriend = True
		profile = target.userinfo_set.all()[0]
		hasProfile = profile.profileSet
	if request.user.pk == pk:
		hasProfile=True
		isFriend = True
		profile = target.userinfo_set.all()[0]
	return render(request=request, template_name="home/Profile.html",context={'target':target,'profile':profile,'isFriend':isFriend,'hasProfile':hasProfile})

def noApplyJobView(request):
	applied = JobUserR.objects.filter(Q(isApply=True))
	print(applied)
	applied = applied.values_list("jid")
	print(applied)
	jobs = Job.objects.exclude(pk__in=applied).exclude(creator=request.user)

	context = {
		"jobs":jobs,
	}
	return render(request=request, template_name="home/notappliedjobs.html",context=context)
def myJobView(request):
	myJobs = Job.objects.filter(creator=request.user)
	relatedJobs = JobUserR.objects.filter(uid=request.user)
	appliedJobs = []
	savedJobs = []
	for jobR in relatedJobs:
		if jobR.isApply:
			appliedJobs.append(jobR.jid)
		if jobR.isStarted:
			savedJobs.append(jobR.jid)
	context = {
		"myJobs": myJobs,
		"appliedJobs": appliedJobs,
		"savedJobs": savedJobs,
	}
	return render(request=request, template_name="home/myjobs.html",context=context)

def jobDetailView(request,pk=None):
	try:
		job = Job.objects.get(pk=pk)
	except:
		messages.error(request,"No Such Job")
		return redirect("home:homepage")
	
	applied = False
	cantApply = False
	saved = False
	if job.creator == request.user:
		cantApply = True
	else:	
		rela = JobUserR.objects.filter(uid=request.user).filter(jid=job)
		if len(rela) != 0:
			if rela[0].isApply:
				applied = True
			if rela[0].isStarted:
				saved = True

	context = {
		"job": job,
		"applied": applied,
		"cantApply": cantApply,
		"saved": saved,
	}
	return render(request=request, template_name="home/jobdetail.html",context=context)

def jobDeleteView(request,pk=None):
	try:
		job = Job.objects.get(pk=pk)
	except:
		messages.error(request,"You cannot delete this job.")
		return redirect("home:homepage")
	if request.user.pk != job.creator.pk:
		messages.error(request,"You cannot delete this job.")
		return redirect("home:homepage")
	
	whoApplied = job.jobuserr_set.filter(isApply=True)
	msg = f"Job \"{job.title}\" is now deleted."
	for applicant in whoApplied:
		newNoti = Notification.objects.create(user=applicant.uid, isAboutJob=True,content=msg
			)
		newNoti.save()
	job.delete()
	messages.success(request,"Job Deleted.")
	return redirect("home:jobs")

def jobApplyView(request,pk=None):
	try:
		job = Job.objects.get(pk=pk)
	except:
		messages.error(request,"No such job.")
		return redirect("home:homepage")
	if job.creator == request.user:
		messages.error(request,"You cannot apply for your own job.")
		return redirect("home:jobs")
	try:
		jur = JobUserR.objects.get(uid=request.user,jid=job,isApply=True)
		messages.error(request,"You have already applied.")
		return redirect("home:jobs")
	except:
		pass	

	form = ApplicationForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			try:
				jur = JobUserR.objects.get(uid=request.user,jid=job,isStarted=True)
				jur.graduationDate = form.cleaned_data["graduationDate"]
				jur.graduationDate = form.cleaned_data["startDate"]
				jur.isApply = True
				jur.isStarted = False
				jur.save()
			except:
				newA = form.save(commit=False)
				newA.uid = request.user
				newA.jid = job
				newA.isApply = True
				newA.isStarted = False
				newA.save()
			messages.success(request,"You application has been made.")
			return redirect("home:detail-job",pk=pk)
	
	context = {
		'form':form,
		'job':job,
	}
	return render(request,"home/jobapply.html",context=context)

def jobSaveView(request,pk=None):
	try:
		job = Job.objects.get(pk=pk)
	except:
		messages.error(request,"No such job.")
		return redirect("home:homepage")

	try:
		jur = JobUserR.objects.get(uid=request.user,jid=job,isApply=True)
		messages.error(request,"You have already applied.")
		return redirect("home:detail-job",pk=pk)
	except:
		pass
	try:
		jur = JobUserR.objects.get(uid=request.user,jid=job,isStarted=True)
		messages.error(request,"You have already saved.")
		return redirect("home:detail-job",pk=pk)
	except:
		pass
	
	try:
		newR = JobUserR.objects.create(jid=job,uid=request.user,isStarted=True,graduationDate=datetime.datetime.now(),startDate=datetime.datetime.now())
		newR.save()
		messages.success(request,"You have saved the job.")
	except:
		messages.error(request,"Fail to save the job.")
		return redirect("home:jobs")

	return redirect("home:detail-job",pk=pk)
def cancelApplyView(request,pk=None):
	try:
		job = Job.objects.get(pk=pk)
		jur = JobUserR.objects.get(uid=request.user,jid=job,isApply=True)
		jur.delete()
		messages.success(request,"You application has been canceled.")
		return redirect("home:detail-job",pk=pk)
	except:
		messages.error(request,"Fail to cancel application.")
		return redirect("home:jobs")
def unsaveView(request,pk=None):
	try:
		job = Job.objects.get(pk=pk)
		jur = JobUserR.objects.get(uid=request.user,jid=job,isStarted=True,isApply=False)
		jur.delete()
		messages.success(request,"Job have been unsaved.")
		return redirect("home:detail-job",pk=pk)
	except Exception as e:
		print(e)
		messages.error(request,"Fail to unsave job.")
		return redirect("home:jobs")
	