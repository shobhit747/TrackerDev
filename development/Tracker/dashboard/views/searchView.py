from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from loginApp.models import Organization
from .basicFunctions import getFamilyDetails,getFamilyMembers,getSingleMember,check
from dashboard.models import Benefit
from datetime import datetime
import calendar

@login_required
def searchView(request):
    user = request.user
    org = Organization.objects.get(user = user)
    if request.method == 'POST':
        familyID = request.POST['familyID']
        aadharNumber = request.POST['aadharNumber']

        # checking for valueError for familyID and aadhar number
        check(familyID)
        check(aadharNumber)
        
        if familyID != '':
            family = getFamilyDetails(familyID)
            if family != 'none':
                return redirect("searchFamilyDetailsView",family_ID = family.family_ID)
        elif aadharNumber != '':
            member = getSingleMember(aadharNumber)
            family = getFamilyDetails(member.belongs_to)

            if family != 'none':
                return redirect("searchFamilyDetailsView",family_ID = family.family_ID)
        


    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
    }
    return render(request,'search.html',sendToTemplate)

@login_required
def searchFamilyDetailsView(request,family_ID):
    user = request.user
    org = Organization.objects.get(user = user)
    family = getFamilyDetails(family_ID)
    members = getFamilyMembers(family_ID)

    createdBy = Organization.objects.get(user = family.created_by_org)
    currentMonth = datetime.now().month
    benefitsReceived = Benefit.objects.filter(given_to = family,date__month = currentMonth).order_by('-date')
    totalAmount = 0
    for benefit in benefitsReceived:
        totalAmount += benefit.amount

    if family.created_by_org == user:
        who = '( You )'

    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'family':family,
        'members':members,
        'createdBy':createdBy,
        'who':who,
        'benefitsReceived':benefitsReceived,
        'currentMonth': calendar.month_name[currentMonth],
        'totalAmount':totalAmount,
    }
    return render(request,"searchFamilyDetails.html",sendToTemplate)

@login_required
def giveBenefitView(request,family_ID):
    user = request.user
    org = Organization.objects.get(user = user)
    family = getFamilyDetails(family_ID)
    members = getFamilyMembers(family_ID)

    createdBy = Organization.objects.get(user = family.created_by_org)

    if family.created_by_org == user:
        who = '( You )'

    if request.method == 'POST':
        
        if request.POST['transactionID'] == '':
            transactionID = 'CASH'
        else:
            transactionID = request.POST['transactionID']
        
        giveBenefit = Benefit(
            given_to = family,
            given_by = org,
            amount = request.POST['amount'],
            transaction_ID = transactionID,
            purpose = request.POST['purpose']
        )

        giveBenefit.save()
        return redirect('searchFamilyDetailsView',family.family_ID)

    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'family':family,
        'members':members,
        'createdBy':createdBy,
        'who':who,
    }
    return render(request,"giveBenefit.html",sendToTemplate)

