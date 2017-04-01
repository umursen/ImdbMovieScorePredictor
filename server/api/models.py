from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name.encode('utf8')


class Writer(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name.encode('utf8')


class Director(models.Model):
    name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name.encode('utf8')


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name.encode('utf8')


class Movie(models.Model):
    name = models.CharField(max_length=128)
    release_date = models.CharField(max_length=64)
    production_budget = models.BigIntegerField(default=0)
    domestic_gross = models.BigIntegerField(default=0)
    worldwide_gross = models.BigIntegerField(default=0)

    casting = models.ManyToManyField(Actor, related_name='casting', blank=True)
    writer = models.ForeignKey(Writer, related_name='writer', null=True, blank=True)
    director = models.ForeignKey(Director, related_name='director', null=True, blank=True)
    rating = models.FloatField(default=0)
    year = models.IntegerField(default=0)
    genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.name.encode('utf8')
