from django.urls import path
from . import views
from .views import addOrEditPageView,searchView,staticsView,beneficiariesView,historyView
urlpatterns = [
    path('statics/',staticsView.staticsView,name='staticsView'),
    path('history/',historyView.historyView,name='historyView'),
    path('historyDetails/<slug:family_ID>/<int:benefit_ID>',historyView.historyDetailsView,name='historyDetailsView'),
    path('beneficiaries/',beneficiariesView.beneficiariesView,name='beneficiariesView'),
    path('search/',searchView.searchView,name='searchView'),
    path('addOrEdit/',addOrEditPageView.addOreditView,name='addOrEditView'),
    path('addOrEditContinue/<slug:family_ID>',addOrEditPageView.addOrEditContinueView,name='addOrEditContinueView'),
    path('familyDetails/<slug:family_ID>',addOrEditPageView.familyDetailsView,name='familyDetailsView'),
    path('searchfamilyDetails/<slug:family_ID>',searchView.searchFamilyDetailsView,name='searchFamilyDetailsView'),
    path('giveBenefit/<slug:family_ID>',searchView.giveBenefitView,name='giveBenefitView'),
]