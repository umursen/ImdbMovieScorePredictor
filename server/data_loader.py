import json
from re import sub

from imdb import IMDb

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from api.models import *
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler

class DataLoader:

    def read_json_file(self):
        with open('../movies.json') as data_file:
            data = json.load(data_file)
            return data

    def populate_django_db(self, movie_limit=1000, cast_limit=10, continue_from=0):
        ia = IMDb()
        data = self.read_json_file()
        saved_movies=0

        for i in range(continue_from, movie_limit):
            currentMovie = data[i]
            basic_movie_info = ia.search_movie(currentMovie['name'])

            if not basic_movie_info:
                continue

            movie_info = ia.get_movie(basic_movie_info[0].movieID)

            if not set(['cast','writer','genres','director','rating']).issubset(set(movie_info.keys())):
                print('Passed one!')
                continue

            if movie_info['kind'].encode('utf-8').strip() == 'movie' and len(movie_info['cast']) >= cast_limit:

                movie, saved = Movie.objects.get_or_create(
                name=currentMovie['name'],
                release_date=currentMovie['release_date'],
                production_budget=sub(r'[^\d.]', '', currentMovie['production_budget']),
                domestic_gross=sub(r'[^\d.]', '', currentMovie['domestic_gross']),
                worldwide_gross=sub(r'[^\d.]', '', currentMovie['worldwide_gross'])
                )

                movie.writer = Writer.objects.get_or_create(name = movie_info['writer'][0]['name'].encode('utf8'))[0]
                movie.director = Director.objects.get_or_create(name = movie_info['director'][0]['name'].encode('utf8'))[0]
                movie.year = movie_info['year']

                if 'rating' in movie_info.keys():
                    movie.rating = movie_info['rating']

                for n in range(cast_limit):
                    movie.casting.add(Actor.objects.get_or_create(name=movie_info['cast'][n]['name'].encode('utf8'))[0])

                for genre in movie_info['genre']:
                    movie.genre.add(Genre.objects.get_or_create(name=genre.encode('utf8'))[0])

                movie.save()

                saved_movies = saved_movies + 1

                print(str(i) + '-) Movie ' + movie.name + ' is saved!')
            else:
                print(str(i) + '-) Error: Couldnt find the movie. Instead, we have ' + currentMovie['name'].encode('utf-8').strip())

        print(str(saved_movies) + ' movies saved out of ' + str(i))


    def load_dataset(self,movie_amount=5000,test_cases=[]):

        actor_amount = len(Actor.objects.all())
        writer_amount = len(Writer.objects.all())
        director_amount = len(Director.objects.all())
        genre_amount = len(Genre.objects.all())

        array_length = actor_amount + writer_amount + director_amount + genre_amount + 1

        X = np.empty([1,array_length], dtype=int)
        y = np.array([], dtype=float)

        movies = Movie.objects.all()

        print('\nCurrently using '+str(len(movies))+' movies for dataset\n')
        print('--Features--\nNumber of Features: 4\nNumber of Actors: '+ str(actor_amount)+'\nNumber of Directors: '+ str(director_amount)+'\nNumber of Writers: '+ str(writer_amount)+'\n')

        for movie in movies:
            m = np.zeros(array_length, dtype=int)

            m[0] = int(str(movie.release_date)[(len(movie.release_date)-4):])

            actor_priority=1
            actor_number = len(movie.casting.all())
            for actor in movie.casting.all():
                m[actor.pk] = actor_priority

            for genre in movie.genre.all():
                m[actor_amount+genre.pk] = 1

            m[actor_amount+genre_amount+movie.writer.pk] = 1
            m[actor_amount+genre_amount+writer_amount+movie.director.pk] = 1

            # m[len(m)-1]=movie.production_budget

            X = np.append(X, [m], axis=0)
            y = np.append(y, movie.rating)
        X = X[1:]
        # THIS PART WILL BE DELETED
        for case in test_cases:
            X = np.append(X,[case],axis=0)

        labelencoder_X_year = LabelEncoder()
        X[:,0] = labelencoder_X_year.fit_transform(X[:,0])
        oneHotEncoder = OneHotEncoder(categorical_features=[0])
        X = oneHotEncoder.fit_transform(X).toarray()
        # X = StandardScaler().transform(X)

        return X,y
