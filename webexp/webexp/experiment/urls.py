from django.urls import path

from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('<uuid:code>/', views.manager, name='manager'),
    path('<uuid:code>/<int:page>/', views.manager, name='session'),
    path('<uuid:code>/ping/', views.ping, name='ping'),
    path('add_codes/<int:number>/', views.codes, name='add_codes'),
    path('delete_data/', views.delete, name='delete_data'),
    # path("clear", views.clear, name = "clear"), # for testing
    path('participants/', views.showParticipants, name='show_participants'),
    path('participant_data/', views.showParticipantLinks, name='show_participants_links'),
    path('data/<uuid:code>/', views.showData, name='show_data'),
    path("download_trials/", views.downloadTrials, name='download_trials'),
    path("download_trials/<str:filename>/", views.downloadTrials, name='download_trials_file'),
    path("download_participants/", views.downloadParticipants, name='download_participants'),
    path("download_participants/<str:filename>/", views.downloadParticipants, name='download_participants_file'),
    path("download_codes/", views.downloadCodes, name='download_codes'),
    path("download_codes/<str:filename>/", views.downloadCodes, name='download_codes_file'),
    path("download_logs/", views.downloadLogs, name='download_logs'),
    path("download_logs/<str:filename>/", views.downloadLogs, name='download_logs_file'),
]