from django.shortcuts import render,redirect
from .models import *
import base64
from django.http import HttpResponse,HttpResponseRedirect
from .py_templates import sr,symptom_finder_ur
from pydub import AudioSegment
from django.contrib import messages
# Create your views here.
from .forms import uploadForm
import datetime
import datetime

dt = datetime.datetime.now().strftime("%Y-%m-%d")
def text(lang):
	#AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"
	#AudioSegment.ffprobe   = r"C:/ffmpeg/bin/ffprobe.exe"
	sound = AudioSegment.from_file("file.oga")
	suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
	filename = "_".join([lang, suffix]) 
	filename='{}.wav'.format(filename)
	sound.export(filename, format="wav")
	tex=sr.takeCommand(filename,lang)
	return tex,filename


def home(request):
	if request.method == 'POST':
		form = uploadForm(request.POST)
		lang=request.POST['language']
		print('lang is', lang)
		if form.is_valid():
			tex,filename=text(lang)
			if tex is not None:
				form.save()
			
				insert = Text.objects.create(texts=tex,filename=filename,upload_text=Upload.objects.last())
				tex=tex.lower()
				symp=symptom_finder_ur.symp_finder(tex,lang)
				print('sympts are',symp)
				if symp is not None:
					#symp=symp.replace(" ",'+')
					print('symptoms are ', symp)
					#for umls db
					#return render(request,'search.html',{'text':tex,'doctor_disease':zip(list(symp['doctor']),list(symp['Disease']))})
					#symp_link='https://ezshifa.com/list.php?speciality={}&typeselect=specility&token=cowciiun5sizsyyzl30fg&idtext={}&visty_type=online&date={}'.format(symp,symp,dt)
					return render(request,'search.html',{'text':tex,'doctor_disease':symp})
					#return redirect(symp_link)
				#messages.success(request,'voice saved')
				else:
					#return redirect('https://ezshifa.com/list.php?speciality=Family%2F+General+%2F+Medical+Physician&typeselect=specility&idselect=&idtext=Family%2F+General+%2F+Medical+Physician&visty_type=online&date='.format(dt))
					return render(request,'search.html',{'text':tex,'doctor_disease':'Family/ General / Medical Physician'})
			else:

				return render(request,'search.html',{'text':'Please speak again'})
	else:
		form = uploadForm()

	return render(request,'home.html',{'load':form})





def search(request):
	if request.method=='POST':
		query=request.POST.get('Search')
		# data=Upload.objects.filter(name__icontains=query)
		# data1=Text.objects.filter(upload_text__in=data)
		#data=Upload.objects.filter(name__icontains=query).prefetch_related('text_set')
		data=Text.objects.filter(upload_text__name__icontains=query)

		return render(request,'search.html',{'query_key':data})
	else:
		pass
	return render(request,'search.html',{'query_key':'Search Value'})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_audio(request):
	print('upload_audio')
	if request.is_ajax():
		
		req=request.POST.get('data')
		d=req.split(",")[1]
		print("Yes, AJAX!")
		#print(request.body)
		f = open('./file.oga', 'wb')
		
		f.write(base64.b64decode(d))
		#f.write(request.body)
		f.close()
	return HttpResponse('audio received')
	

#