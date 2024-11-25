from django.contrib import admin
from users.models import UserModel, VerificationModel



admin.site.register(VerificationModel)

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')