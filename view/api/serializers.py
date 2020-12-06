from rest_framework import serializers
from view.models import ViewUser
class ViewUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=ViewUser
        fields=['id', 'username', 'MacAdd', 'url', 'connect', 'lastLogin']
