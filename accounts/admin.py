from django.contrib import admin
from .models import User, AccessCode

admin.site.register(User)
admin.site.register(AccessCode)