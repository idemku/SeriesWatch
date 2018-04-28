##
# @file
# File documentation
#

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SeriesTable, User

admin.site.register(SeriesTable)
admin.site.register(User, UserAdmin)
