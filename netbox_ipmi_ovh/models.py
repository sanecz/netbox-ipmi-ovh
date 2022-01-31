from django.db import models
from django.contrib.auth.models import User


__all__ = ("Ipmi",)

class Ipmi(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="ipmi",
        editable=False
    )

    ssh_key_name = models.TextField(
        verbose_name="SSH key name"
    )

    ip_to_allow = models.TextField(
        verbose_name="IP to allow"
    )

    class Meta:
        verbose_name = "IPMI"
        permissions = [('view_ipmi', 'Can use IPMI')]
        default_permissions = []
