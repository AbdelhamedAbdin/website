from rest_framework import generics, permissions
from .serializers import UserProfileRetrieveSerializer
from accounts.models import UserProfile
from rest_framework.response import Response


class UserProfileRetrieveView(generics.RetrieveUpdateAPIView,
                              generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    lookup_field = 'slug'
    serializer_class = UserProfileRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, slug=None, **kwargs):
        userprofile = UserProfile.objects.get(slug=slug)
        serializer = UserProfileRetrieveSerializer(userprofile, many=False)
        if slug:
            if self.request.user.userprofile != slug:
                return self.retrieve(request, slug=slug)
        return Response(data=serializer.data)
