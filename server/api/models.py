from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=128, unique=True)
    release_date = models.CharField(max_length=64)
    production_budget = models.BigIntegerField(default=0)
    domestic_gross = models.BigIntegerField(default=0)
    worldwide_gross = models.BigIntegerField(default=0)

    casting = models.ManyToManyField(Person, related_name='casting', blank=True, null=True)
    writer = models.ForeignKey(Person,  related_name='writer', null=True, blank=True)
    director = models.ForeignKey(Person,  related_name='director', null=True, blank=True)
    rating = models.FloatField(default=0)
    year = models.IntegerField(default=0)
    genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.name
