import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
import numpy as np
from api.models import *

class DataConverter:

    def __init__(self):
        self.actor_amount = len(Actor.objects.all())
        self.writer_amount = len(Writer.objects.all())
        self.director_amount = len(Director.objects.all())
        self.genre_amount = len(Genre.objects.all())
        self.array_length = self.actor_amount + self.writer_amount + self.director_amount + self.genre_amount + 1
        print(self.array_length)

    def convert_casting(self,actors):
        actor_indexes = []
        for actor_name in actors:
            actor = Actor.objects.get(name=actor_name)
            if actor:
                actor_indexes.append(actor.pk)
            else:
                print('Error')
        return actor_indexes

    def convert_genres(self,genres):
        genre_indexes = []
        for genre_name in genres:
            genre = Genre.objects.get(name=genre_name)
            if genre:
                genre_indexes.append(genre.pk)
            else:
                print('Error')
        return genre_indexes

    def convert_writer(self,writer_name):
        writer = Writer.objects.get(name=writer_name)
        if writer:
            return writer.pk
        else:
            print('Error')

    def convert_director(self,director_name):
        director = Director.objects.get(name=director_name)
        if director:
            return director.pk
        else:
            print('Error')

    def create_movie(self,casting,release_date,genres,writer,director):
        casting = self.convert_casting(casting)
        genres = self.convert_genres(genres)
        writer = self.convert_writer(writer)
        director = self.convert_director(director)

        X = np.zeros(self.array_length, dtype=int)

        X[0] = release_date

        for actor_index in casting:
            X[actor_index] = 1

        for genre_index in genres:
            X[self.actor_amount+genre_index] = 1

        X[self.actor_amount+self.genre_amount+writer] = 1
        X[self.actor_amount+self.genre_amount+self.writer_amount+director] = 1

        return X
