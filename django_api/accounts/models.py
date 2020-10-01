from django.db import models


class UserLoginHistory(models.Model):
    """Model to keep a history of ip address for logins"""

    # class Meta:
    #     ordering = True

    user_id = models.CharField(max_length=128)
    ip_addr = models.GenericIPAddressField()
    time = models.DateTimeField(auto_now_add=True)
