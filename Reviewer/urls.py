from django.urls import path
from . import views

# Url Mappings for the Reviewer View of the CPMS website. 

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('reviewerDownloadPapers', views.reviewerDownloadPapers, name='reviewerDownloadPapers'),
    path('reviewerModifyInfo', views.reviewerModifyInfo, name='reviewerModifyInfo'),
    path('reviewerRegisterToReviewPapers', views.reviewerRegisterToReviewPapers, name='reviewerRegisterToReviewPapers'),
    path('reviewerReviewPapers', views.reviewerReviewPapers, name='reviewerReviewPapers'),
]
