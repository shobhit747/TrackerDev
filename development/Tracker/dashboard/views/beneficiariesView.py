from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from loginApp.models import Organization
from dashboard.models import FamilyModel,memberOfaFamily,Benefit
import random

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


@login_required
def beneficiariesView(request):
    user = request.user
    org = Organization.objects.get(user = user)

    familiesAdded = FamilyModel.objects.filter(created_by_org = user).order_by('-date_created')
    print(familiesAdded)
    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'familiesAdded':familiesAdded,
    }
    return render(request,'beneficiaries.html',sendToTemplate)