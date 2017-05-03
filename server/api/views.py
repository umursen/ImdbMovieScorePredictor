from django.shortcuts import render, render_to_response
from api.models import *
from django.http import JsonResponse
from django.template import RequestContext
import pickle
from data_converter import DataConverter

def index(request):
    return render(request, 'index.html',{'score':0})

def predict(request):
    if request.POST:
        model = pickle.load(open('finalized_model.sav', 'rb'))

        actors = map(int,request.POST.getlist('actors[]'))
        genres = map(int,request.POST.getlist('genres[]'))
        director = int(request.POST.get('director',''))
        writer = int(request.POST.get('writer',''))
        year = int(request.POST.get('year',''))
        score = model.predict(DataConverter().create_movie([actors,genres,director,writer,year],True))

    return render(request,'index.html',{'score':score[0]})
