from django.core.exceptions import ObjectDoesNotExist
from dashboard.models import FamilyModel,memberOfaFamily
import random

def generateFamilyID():
    id = random.randint(100000,999999)
    return str(id)

def getFamilyDetails(familyID):
    try:
        family = FamilyModel.objects.get(family_ID = familyID)
        return family
    except FamilyModel.DoesNotExist:
        return 'none'

def getFamilyMembers(familyID):
    try:
        family = getFamilyDetails(familyID)
        members = memberOfaFamily.objects.filter(belongs_to = family)
        return members
    except ObjectDoesNotExist:
        print("none")
        
def getSingleMember(aadhar):
    try:
        member = memberOfaFamily.objects.get(aadhar = aadhar)
        return member
    except ObjectDoesNotExist:
        return 'does not exist'


#handling valueError with check functions 
def check(thisValue:int):
        try:
            r = int(thisValue)
            return r
        except ValueError:
            return "invalid"
        
def deleteNotSaved(user):
    families = FamilyModel.objects.filter(created_by_org = user,in_public_domain = False)
    for f in families:
        print(f)
    families.delete()
    print("Deleted")