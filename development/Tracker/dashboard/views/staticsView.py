from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from loginApp.models import Organization
from dashboard.models import FamilyModel,memberOfaFamily,Benefit

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .basicFunctions import getFamilyDetails,getFamilyMembers,getSingleMember,generateFamilyID
from django.db.models import Sum
from datetime import datetime,timedelta
import calendar
@login_required
def staticsView(request):
    user = request.user
    org = Organization.objects.get(user = user)

    if org.aboutOrg == 'none' or org.localAddress == 'none':
        return redirect('registrationOrgInfoView')
    if org.mobile == 'none':
        return redirect('registrationSendOtpView')

    families = FamilyModel.objects.filter(created_by_org = user)
    amounts = Benefit.objects.filter(given_by = org)
    totalSpend = 0
    for a in amounts:
        totalSpend += a.amount
    currentMonth = datetime.now().month
    monthsAmounts = Benefit.objects.filter(given_by = org,date__month = currentMonth)
    totalAmtByMonth = 0
    for benefit in monthsAmounts:
        totalAmtByMonth += benefit.amount
    print(totalAmtByMonth)
    famliesAddedThisMonth = families.filter(date_created__month = currentMonth).count()
    print(famliesAddedThisMonth)
    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'currentMonth':calendar.month_name[currentMonth],
        'totalSpend':totalSpend,
        'thisMonthsSpend':totalAmtByMonth,
        'totalBeneficiary':families.count(),
        'famliesAddedThisMonth':famliesAddedThisMonth,
        'benefitedThisMonth':monthsAmounts.values('given_to').distinct().count()
    }
    return render(request,'statics.html',sendToTemplate)