from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from events.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CountryCreateApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class EventsApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class AthleteUpdateApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

class CommentDeleteApi(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
