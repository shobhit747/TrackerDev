from django.contrib import admin
from .models import FamilyModel,memberOfaFamily,Benefit
# Register your models here.

admin.site.register(FamilyModel)
admin.site.register(memberOfaFamily)
admin.site.register(Benefit)
