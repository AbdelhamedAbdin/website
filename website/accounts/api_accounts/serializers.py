from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from accounts.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="api_accounts:detail",
        lookup_field='slug'
    )

    class Meta:
        model = UserProfile
        fields = ['overview', 'city', 'sex', 'phone', 'skill', 'logo', 'slug', 'url']


class UserProfileRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['overview', 'city', 'sex', 'phone', 'skill']
