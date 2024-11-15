from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)


class VerificationModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='verification')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.code}'

    class Meta:
        verbose_name = 'Verification'
        verbose_name_plural = 'Verifications'
        unique_together = ('user', 'code')

