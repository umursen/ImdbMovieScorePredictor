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

    def save_ids(self):
        actors = Actor.objects.all()
        data = {}
        for actor in actors:
            data[actor._id] = ''
        with open('actor_ids.json', 'w') as outfile:
            json.dump(data, outfile)

        writers = Writer.objects.all()
        data = {}
        for writer in writers:
            data[writer._id] = ''
        with open('writer_ids.json', 'w') as outfile:
            json.dump(data, outfile)

        directors = Director.objects.all()
        data = {}
        for director in directors:
            data[director._id] = ''
        with open('director_ids.json', 'w') as outfile:
            json.dump(data, outfile)

    def set_poster_urls(self):
        with open('../ActorCrawler/actor_posters.json') as data_file:
            data = json.load(data_file)
            for poster_data in data:
                poster_url = poster_data['poster']
                user_id = poster_data['id']
                person = Actor.objects.get(_id=int(user_id))
                person.poster = poster_url
                person.save()

        with open('../ActorCrawler/director_posters.json') as data_file:
            data = json.load(data_file)
            for poster_data in data:
                poster_url = poster_data['poster']
                user_id = poster_data['id']
                person = Director.objects.get(_id=int(user_id))
                person.poster = poster_url
                person.save()

        with open('../ActorCrawler/writer_posters.json') as data_file:
            data = json.load(data_file)
            for poster_data in data:
                poster_url = poster_data['poster']
                user_id = poster_data['id']
                actor = Writer.objects.get(_id=int(user_id))
                actor.poster = poster_url
                actor.save()

        print('Poster urls are saved')

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
                movie.writer._id=int(movie_info['writer'][0].personID)
                movie.writer.save()

                movie.director = Director.objects.get_or_create(name = movie_info['director'][0]['name'].encode('utf8'), _id=int(movie_info['director'][0].personID))[0]
                movie.year = Year.objects.get_or_create(year = movie_info['year'])[0]

                if 'rating' in movie_info.keys():
                    movie.rating = movie_info['rating']

                for n in range(cast_limit):
                    actor = Actor.objects.get_or_create(name=movie_info['cast'][n]['name'].encode('utf8'))[0]
                    actor._id=int(movie_info['cast'][n].personID)
                    actor.save()
                    movie.casting.add(actor)

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
        year_amount = len(Year.objects.all())

        array_length = actor_amount + writer_amount + director_amount + genre_amount + year_amount

        X = np.empty([1,array_length], dtype=int)
        y = np.array([], dtype=float)

        movies = Movie.objects.all()

        print('\nCurrently using '+str(len(movies))+' movies for dataset\n')
        print('--Features--\nNumber of Features: 4\nNumber of Actors: '+ str(actor_amount)+'\nNumber of Directors: '+ str(director_amount)+'\nNumber of Writers: '+ str(writer_amount)+'\nNumber of Years: '+ str(year_amount)+'\n')

        for movie in movies:
            m = np.zeros(array_length, dtype=int)

            for actor in movie.casting.all():
                m[actor.pk-1] = 1

            for genre in movie.genre.all():
                m[actor_amount+genre.pk-1] = 1

            m[actor_amount+genre_amount+movie.writer.pk-1] = 1
            m[actor_amount+genre_amount+writer_amount+movie.director.pk-1] = 1
            m[actor_amount+genre_amount+writer_amount+director_amount+movie.year.pk-1] = 1

            # m[len(m)-1]=movie.production_budget

            X = np.append(X, [m], axis=0)
            y = np.append(y, movie.rating)
        X = X[1:]

        # labelencoder_X_year = LabelEncoder()
        # X[:,0] = labelencoder_X_year.fit_transform(X[:,0])
        # oneHotEncoder = OneHotEncoder(categorical_features=[0])
        # X = oneHotEncoder.fit_transform(X).toarray()

        # X = StandardScaler().transform(X)

        return X,y
