from django.shortcuts import render, render_to_response
from api.models import *
from django.http import JsonResponse
from django.template import RequestContext
import pickle
from data_converter import DataConverter
import ast

def index(request):
    return render(request, 'index.html',{'score':0})

def predict(request):
    if request.POST:
        model = pickle.load(open('finalized_model.sav', 'rb'))
        actors = []
        n=0
        for actor in request.POST.getlist('actors[]'):
            actors.append(ast.literal_eval(actor)['id'])
        actors = map(int,actors)
        genres = map(int,request.POST.getlist('genres[]'))
        director = int(ast.literal_eval(request.POST.get('director',''))['id'])
        writer = int(ast.literal_eval(request.POST.get('writer',''))['id'])
        year = int(request.POST.get('year',''))
        score = model.predict(DataConverter().create_movie([actors,genres,director,writer,year],True))[0]
        percentage = int(score)*10
    return render(request,'index.html',{'score':float("{0:.2f}".format(score)), 'percentage': percentage, 's_actors': actors, 's_genres':genres,'s_director':director,'s_writer':writer,'s_year':year})
