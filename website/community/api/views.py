from rest_framework import generics, permissions
from .serializers import CommunitySerializer, CommunityDteailSerializer
from community.models import UserAsking
from accounts.models import UserProfile
from django.http import HttpResponse


class CommunityListView(generics.ListAPIView, generics.ListCreateAPIView):
    serializer_class = CommunitySerializer
    queryset = UserAsking.objects.all()
    # lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]


class CommunityDetailView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    serializer_class = CommunityDteailSerializer
    queryset = UserAsking.objects.all()
    lookup_field = 'ask_slug'
    permission_classes = []
