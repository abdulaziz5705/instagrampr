from django.db.migrations import CreateModel
from rest_framework import serializers

from comment.models import TweetModel, CommentModel
from users.serializers import UsersSerializer

class TweetSerializer(serializers.ModelSerializer):
   child_count = serializers.SerializerMethodField(method_name='get_child_count')

   class Meta:
       model = TweetModel
       fields = ['id', 'text', 'child_count', 'parent', 'created_at', 'image']
       extra_kwargs = {
           'parent': {'read_only': True},
           'created_at': {'read_only': True},
           'image': {'read_only': True},
       }

   def get_child_count(self, obj):
        return obj.child_set.count()

class TweetCommentSerializer(serializers.ModelSerializer):
     child_count = serializers.SerializerMethodField(method_name='get_child_count')
     user = UsersSerializer(read_only=True)
     tweet = serializers.PrimaryKeyRelatedField(queryset=TweetModel.objects.all())

     class Meta:
             model = CommentModel
             fields = ['id', 'comment', 'user', 'child_count', 'created_at', 'parent', 'tweet ']
             extra_kwargs = {
                 'parent': {'read_only': False},
             }

     @staticmethod
     def get_child_count(self, obj):
           return obj.child_set.count()


