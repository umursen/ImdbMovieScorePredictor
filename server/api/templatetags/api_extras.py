from django import template
from api.models import *

register = template.Library()

@register.inclusion_tag("actors.html")
def list_actors():
    try:
        actors = Actor.objects.all()
    except Actor.DoesNotExist:
        pass
    return {'actors': actors}

@register.inclusion_tag("writers.html")
def list_writers():
    try:
        writers = Writer.objects.all()
    except Writer.DoesNotExist:
        pass
    return {'writers': writers}

@register.inclusion_tag("directors.html")
def list_directors():
    try:
        directors = Director.objects.all()
    except Director.DoesNotExist:
        pass
    return {'directors': directors}

@register.inclusion_tag("years.html")
def list_years():
    try:
        years = Year.objects.all()
    except Year.DoesNotExist:
        pass
    return {'years': years}

@register.inclusion_tag("genres.html")
def list_genres():
    try:
        genres = Genre.objects.all()
    except Genre.DoesNotExist:
        pass
    return {'genres': genres}
