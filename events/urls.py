from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

app_name='events'


urlpatterns = [
    path('', views.EventListView.as_view()),
    path('events', views.EventListView.as_view(), name='all'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('event/create',
        views.EventCreateView.as_view(success_url=reverse_lazy('events:all')), name='event_create'),
    path('event/<int:pk>/update',
        views.EventUpdateView.as_view(success_url=reverse_lazy('events:all')), name='event_update'),
    path('event/<int:pk>/delete',
        views.EventDeleteView.as_view(success_url=reverse_lazy('events:all')), name='event_delete'),
    path('event_picture/<int:pk>', views.stream_file, name='event_picture'),
    path('event/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='event_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('events')), name='event_comment_delete'),
    path('event/<int:pk>/important',
    views.AddImportantView.as_view(), name='event_important'),
    path('event/<int:pk>/unimportant',
    views.DeleteImportantView.as_view(), name='event_unimportant'),
    path('event/news',
    views.sendNewsData, name='event_news'),
    path('event/hotels',
    views.sendHotels, name='event_hotels'),
]
