# from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
# from loginApp.models import Organization
# from .models import FamilyModel,memberOfaFamily
# import random

# from django.core.exceptions import ObjectDoesNotExist
# from django.db import IntegrityError

# # normal functions

# def getFamilyDetails(familyID):
#     try:
#         family = FamilyModel.objects.get(family_ID = familyID)
#         return family
#     except family.DoesNotExists:
#         print("none")

# def getFamilyMembers(familyID):
#     try:
#         family = getFamilyDetails(familyID)
#         members = memberOfaFamily.objects.filter(belongs_to = family)
#         return members
#     except ObjectDoesNotExist:
#         print("none")

# def getSingleMember(aadhar):
#     try:
#         member = memberOfaFamily.objects.get(aadhar = aadhar)
#         return member
#     except ObjectDoesNotExist:
#         return 'does not exist'
    
# #django views

# @login_required
# def staticsView(request):
#     user = request.user
#     org = Organization.objects.get(user = user)

#     sendToTemplate = {
#         'organizationLoggedIn': str(org).capitalize,
#     }
#     return render(request,'statics.html',sendToTemplate)

# @login_required
# def historyView(request):
#     return render(request,'history.html')

# @login_required
# def beneficiariesView(request):
#     return render(request,'beneficiaries.html')

# @login_required
# def searchView(request):
#     return render(request,'search.html')

# def generateFamilyID():
#     id = random.randint(100000,999999)
#     return str(id)

# @login_required
# def addOreditView(request):
#     user = request.user
#     org = Organization.objects.get(user = user)

#     if request.method == 'POST':
#         try:
#             family = FamilyModel.objects.get(phone_number = request.POST['PhoneNo'])
#             return redirect('addOrEditContinueView',family_ID = family.family_ID)
#         except ObjectDoesNotExist:
#             while True:
#                 familyID = generateFamilyID()
#                 idExists = FamilyModel.objects.filter(family_ID = familyID).exists()
#                 if idExists:
#                     continue
#                 else:
#                     createFamoly = FamilyModel(
#                     family_ID = familyID,
#                     phone_number=request.POST['PhoneNo'],
#                     created_by_org=user
#                     )
#                     createFamoly.save()
#                     return redirect('addOrEditContinueView',family_ID = familyID)
#                     break
#     sendToTemplate = {
#         'organizationLoggedIn': str(org).capitalize,
#     }
#     return render(request,'addOredit.html',sendToTemplate)

# @login_required
# def addOrEditContinueView(request,family_ID):
#     user = request.user
#     org = Organization.objects.get(user = user)

#     family = getFamilyDetails(family_ID)
#     members = getFamilyMembers(family_ID)
#     error = False
#     #handling valueError with check function
#     def check(thisValue):
#         try:
#             r = int(thisValue)
#             return r
#         except ValueError:
#             return "invalid"
    
#     if request.method == 'POST':
#         print(request.POST)
#         if 'addingMember' in request.POST:
#             name = request.POST['name']
#             aadhar = check(request.POST['aadhar'])
#             age = check(request.POST['age'])
#             gender = request.POST['gender']

#             if aadhar != "invalid" and age != "invalid":
#                 try:
#                     member = memberOfaFamily(
#                         name = name,
#                         aadhar = aadhar,
#                         age = age,
#                         gender = gender,
#                         belongs_to = family
#                     )
#                     member.save()
#                 except IntegrityError:
#                     error = True
                    
#         if 'deleting' in request.POST:
#             memberToDelete = getSingleMember( aadhar = request.POST['deleteAadharMember'] ) 
#             memberToDelete.delete()
#             print('member deleted')

#         if 'addOrEditAddress' in request.POST:
#             family.residential_address = request.POST['address']
#             family.save() 

#         if 'finalSave' in request.POST:
#             family.in_public_domain = True
#             family.save()
#             return redirect('familyDetailsView',family_ID = family_ID)
            

#     alreadyExists = "Aadhar number already exists."
#     address = family.residential_address

#     sendToTemplate = {
#         'organizationLoggedIn': str(org).capitalize,
#         'familyID':family.family_ID,
#         'familyPhoneNumber':family.phone_number,
#         'familyAddress':family.residential_address,
#         'members':members,
#         'alreadyExists': alreadyExists,
#         'address':address,
#         'error':error
#     }
#     return render(request,'addOrEditContinue.html',sendToTemplate)

# def familyDetailsView(request,family_ID):
#     user = request.user
#     org = Organization.objects.get(user = user)
#     sendToTemplate = {
#         'organizationLoggedIn': str(org).capitalize,
#     }
#     return render(request,'familyDetails.html',sendToTemplate)