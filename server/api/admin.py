from django.contrib import admin
from api.models import *

admin.site.register([Movie, Actor, Writer, Director, Genre])
