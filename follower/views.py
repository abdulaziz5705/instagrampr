from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from follower.models import FollowingModel
from follower.serializer import FollowerSerializer


class FollowingView(APIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)


        user = self.request.user
        to_user = serializer.validated_data['to_user']
        response = {"success": True}

        following = FollowingModel.objects.filter(user=user, to_user=to_user)
        if following.exists():
            following.delete()
            response['detail'] = "You have unfollowing successfully"
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        FollowingModel.objects.create(user=user, to_user=to_user)
        response['detail'] = "You have following successfully"

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        follow_type = self.request.query_params.get('type')
        fl = self.request.user.following.all()
        if follow_type == "followers":
            fl = self.request.user.following.all()
        serializer = FollowerSerializer(fl, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

