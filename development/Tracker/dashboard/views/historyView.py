from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from loginApp.models import Organization
from dashboard.models import FamilyModel,memberOfaFamily,Benefit
import random
from .basicFunctions import getFamilyDetails,getFamilyMembers,getSingleMember,check
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

@login_required
def historyView(request):
    user = request.user
    org = Organization.objects.get(user = user)
    
    benefitsHistory = Benefit.objects.filter(given_by = org).order_by('-id')

    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'benefitsHistory':benefitsHistory,
    }
    return render(request,'history.html',sendToTemplate)

@login_required
def historyDetailsView(request,family_ID,benefit_ID):
    user = request.user
    org = Organization.objects.get(user = user)
    family = getFamilyDetails(family_ID)
    members = getFamilyMembers(family_ID)
    createdBy = Organization.objects.get(user = family.created_by_org)


    benefit = Benefit.objects.get(id = benefit_ID)
    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'benefit':benefit,
        'family':family,
        'members':members,
        'createdBy':createdBy,
    }

    if benefit.given_by == org:
        who = '( You )'
        sendToTemplate['who'] = who
        return render(request,'historyDetails.html',sendToTemplate)
    else:
        return redirect(request,historyView)