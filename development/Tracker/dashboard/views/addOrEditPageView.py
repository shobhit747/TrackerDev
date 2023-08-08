from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from loginApp.models import Organization
from dashboard.models import FamilyModel,memberOfaFamily

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .basicFunctions import getFamilyDetails,getFamilyMembers,getSingleMember,generateFamilyID,check,deleteNotSaved
@login_required
def addOreditView(request):
    user = request.user
    org = Organization.objects.get(user = user)

    deleteNotSaved(user)

    if request.method == 'POST':
        try:
            family = FamilyModel.objects.get(phone_number = request.POST['PhoneNo'])
            return redirect('addOrEditContinueView',family_ID = family.family_ID)
        except ObjectDoesNotExist:
            while True:
                familyID = generateFamilyID()
                idExists = FamilyModel.objects.filter(family_ID = familyID).exists()
                if idExists:
                    continue
                else:
                    createFamoly = FamilyModel(
                    family_ID = familyID,
                    phone_number=request.POST['PhoneNo'],
                    created_by_org=user
                    )
                    createFamoly.save()

                    return redirect('addOrEditContinueView',family_ID = familyID)
                    break
    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
    }
    return render(request,'addOrEdit.html',sendToTemplate)

@login_required
def addOrEditContinueView(request,family_ID):
    user = request.user
    org = Organization.objects.get(user = user)
    family = getFamilyDetails(family_ID)
    members = getFamilyMembers(family_ID)
    error = False
    # data = request.session['addFamily']

    if family.created_by_org != user :
        return redirect('familyDetailsView',family_ID = family_ID)
    
    if request.method == 'POST':
        if 'addingMember' in request.POST:
            name = request.POST['name']
            aadhar = check(request.POST['aadhar'])
            age = check(request.POST['age'])
            gender = request.POST['gender']
            if aadhar != "invalid" and age != "invalid":
                try:
                    member = memberOfaFamily(
                        name = name,
                        aadhar = aadhar,
                        age = age,
                        gender = gender,
                        belongs_to = family
                    )
                    member.save()
                except IntegrityError:
                    error = True
        if 'deleting' in request.POST:
            memberToDelete = getSingleMember( aadhar = request.POST['deleteAadharMember'] ) 
            memberToDelete.delete()
            print('member deleted')

        if 'addOrEditAddress' in request.POST:
            family.residential_address = request.POST['address']
            family.save()

        if 'finalSave' in request.POST:
            family.in_public_domain = True
            family.save()
            return redirect('familyDetailsView',family_ID = family_ID)
            

    alreadyExists = "Aadhar number already exists."
    address = family.residential_address
    if address == 'none':
        address = ''
    print(members.count())
    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'familyID':family.family_ID,
        'familyPhoneNumber':family.phone_number,
        'familyAddress':address,
        'members':members,
        'alreadyExists': alreadyExists,
        'error':error,
        'noWarning':family.in_public_domain
    }
    return render(request,'addOrEditContinue.html',sendToTemplate)

@login_required
def familyDetailsView(request,family_ID):
    user = request.user
    org = Organization.objects.get(user = user)

    family = getFamilyDetails(family_ID)
    members = getFamilyMembers(family_ID)
    createdBy = Organization.objects.get(user = family.created_by_org)

    if family.created_by_org == user:
        who = '( You )'
    sendToTemplate = {
        'organizationLoggedIn': str(org).capitalize,
        'family': family,
        'members' : members,
        'createdBy':createdBy,
        'who':who,
    }
    return render(request,'familyDetails.html',sendToTemplate)