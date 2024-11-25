from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from comment.models import TweetModel, CommentModel
from comment.serializers import TweetSerializer, TweetCommentSerializer
from rest_framework import generics

class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = TweetSerializer
    queryset = TweetModel.objects.all()
    permission_classes = [ IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return TweetModel.objects.filter(parent__isnull=True)


class TweetChildListApiView(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [ IsAuthenticated]

    def get_queryset(self):
        parent = self.request.query_params.get('parent')
        if parent is None:
            return []
        return TweetModel.objecgts.filter(parent__id=parent)

class TweetCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TweetCommentSerializer
    queryset = CommentModel.objects.all()
    permission_classes = [ IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CommentModel.objects.filter(parent__isnull=True)