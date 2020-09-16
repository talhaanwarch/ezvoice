from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
	if request.method=='POST':
		name=request.POST['Name'] #here Name is from form name
		email=request.POST['email']#here email is from form email name
		submit =Upload(name=name,email=email)
		submit.save()
	return render(request,template_name='home.html',context={'print':'ok'})

def search(request):
	if request.method=='POST':
		query=request.POST.get('Search')
		data=Upload.objects.filter(name__icontains=query)
		return render(request,'search.html',{'query_key':data})
	else:
		pass
	return render(request,'search.html',{'query_key':'Search Value'})