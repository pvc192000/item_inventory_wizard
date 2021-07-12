from django.urls import path
from . import views

# Url Mappings for the Administrator View of the CPMS website. 

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('maintainAuthors', views.maintainAuthors, name='maintainAuthors'),
    path('maintainPapers', views.maintainPapers, name='maintainPapers'),
    path('maintainReviewers', views.maintainReviewers, name='maintainReviewers'),
    path('maintainReviews', views.maintainReviews, name='maintainReviews'),
    path('managePaperReviewAcceptance', views.managePaperReviewAcceptance, name='managePaperReviewAcceptance'),
    path('matchPaperWithReviewers', views.matchPaperWithReviewers, name='matchPaperWithReviewers'),
    path('maintainAuthors', views.maintainAuthors, name='maintainAuthors'),
    path('authorsReport', views.authorsReport, name='authorsReport'),
    path('reviewersCommentsReport', views.reviewersCommentsReport, name='reviewersCommentsReport'),
    path('reviewersReport', views.reviewersReport, name='reviewersReport'),
    path('reviewsSummaryReport', views.reviewsSummaryReport, name='reviewsSummaryReport'),
    path('insertAuthors', views.insertAuthors, name='insertAuthors'),
    path('updateAuthors', views.updateAuthors, name='updateAuthors'),
    path('deleteAuthors', views.deleteAuthors, name='deleteAuthors'),
    path('insertPapers', views.insertPapers, name='insertPapers'),
    path('updatePapers', views.updatePapers, name='updatePapers'),
    path('deletePapers', views.deletePapers, name='deletePapers'),
    path('insertReviewers', views.insertReviewers, name='insertReviewers'),
    path('updateReviewers', views.updateReviewers, name='updateReviewers'),
    path('deleteReviewers', views.deleteReviewers, name='deleteReviewers'),
    path('insertReviews', views.insertReviews, name='insertReviews'),
    path('updateReviews', views.updateReviews, name='updateReviews'),
    path('deleteReviews', views.deleteReviews, name='deleteReviews'),
]
