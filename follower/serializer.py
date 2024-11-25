from rest_framework import serializers

from follower.models import FollowingModel
from users.models import UserModel


class FollowerSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())


    class Meta:
        model = FollowingModel
        fields = ['created_at', 'to_user']
    @staticmethod
    def is_following_back(obj):
        return FollowingModel.objects.filter(user=obj.to_user, to_user=obj.user).exists()

    def to_representation(self, instance):
        data = dict()
        data['id'] = instance.to_user.id
        data['username'] = instance.to_user.username
        data['first_name']= instance.to_user.first_name
        data['last_name']= instance.to_user.last_name
        data['email']= instance.to_user.email
        data['following_back']= self.is_following_back(instance)
        return data
