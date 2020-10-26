from rest_framework import serializers
from community.models import UserAsking
from django.contrib.auth.models import User


class CommunitySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:question-detail',
        lookup_field='ask_slug'
    )

    class Meta:
        model = UserAsking
        fields = ['title', 'question', 'field', 'date', 'userprofile', 'url']


class CommunityDteailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAsking
        fields = ['title', 'question', 'field']
