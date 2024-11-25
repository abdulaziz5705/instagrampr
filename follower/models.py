from django.db import models

from users.models import UserModel


class FollowingModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} following to {self.to_user.email}'


