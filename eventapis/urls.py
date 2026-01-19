from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('create_country',CountryCreateApi.as_view()),
    path('events_list',EventsApi.as_view()),
    path('update_athlete/<int:pk>',AthleteUpdateApi.as_view()),
    path('delete_comment/<int:pk>',CommentDeleteApi.as_view()),
    path('api/token/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),

]
