import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from api.models import *


def getActingListPerActor():
    movies = Movie.objects.all()
    actingList = [0]*len(Actor.objects.all())
    for movie in movies:
        casting = movie.casting.all()
        for actor in casting:
            actingList[actor.pk-1] = actingList[actor.pk-1] + 1
    return actingList

def actingMean():
    actingList = getActingListPerActor()
    return float(sum(actingList)/len(actingList))

def actingVariance():
    actingList = getActingListPerActor()
    mean = actingMean()
    variance = reduce(lambda x, y: (x - mean)**2 + (y - mean)**2, actingList)
    return variance

def actingStandardDeviation():
    variance = actingVariance()
    return sqrt(variance)

if __name__ == '__main__':
    print('Mean is ' + str(actingMean()))
    print('Variance is ' + str(actingVariance()))
    print('StandardDeviation is ' + str(actingStandardDeviation()))
