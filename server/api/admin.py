from django.contrib import admin
from api.models import *

admin.site.register([Movie, Person, Genre])
