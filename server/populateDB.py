import json
from re import sub

from imdb import IMDb

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from api.models import *

def readJSONFile():
    with open('../movies.json') as data_file:
        data = json.load(data_file)
        return data

def importCast(movieInfo, castRange=10):
    return

def populateDjangoDB(data, movieNumber=500):

    savedMovies=0

    for i in range(movieNumber):
        currentMovie = data[i]
        basicMovieInfo = ia.search_movie(currentMovie['name'])
        movieInfo = ia.get_movie(basicMovieInfo[0].movieID)

        if str(movieInfo['kind']) == 'movie':
            movie = Movie.objects.get_or_create(
            name=currentMovie['name'],
            release_date=currentMovie['release_date'],
            production_budget=sub(r'[^\d.]', '', currentMovie['production_budget']),
            domestic_gross=sub(r'[^\d.]', '', currentMovie['domestic_gross']),
            worldwide_gross=sub(r'[^\d.]', '', currentMovie['worldwide_gross']),
            )[0]

            movie.writer = Person.objects.get_or_create(name = str(movieInfo['writer'][0]['name']))[0]
            movie.director = Person.objects.get_or_create(name = str(movieInfo['director'][0]['name']))[0]
            movie.rating = movieInfo['rating']
            movie.year = movieInfo['year']

            for person in movieInfo['casting']:
                movie.casting.add(Person.objects.get_or_create(name=str(person['name']))[0])

            for genre in movieInfo['genre']:
                movie.genre.add(Genre.objects.get_or_create(name=str(genre))[0])

            movie.save()

            savedMovies = savedMovies + 1
            print('Movie ' + movie.name + ' is saved!')

    print(str(savedMovies) + ' movies saved out of ' + str(i))



if __name__ == '__main__':
    ia = IMDb()
    data = readJSONFile()
    populateDjangoDB(data)
