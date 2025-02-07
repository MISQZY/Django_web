from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class Sniffing(models.Model):
    enabled = models.BooleanField(default=False)
    dest_override = models.JSONField(default=list)
    metadata_only = models.BooleanField(default=False)
    route_only = models.BooleanField(default=False)

class StreamSettings(models.Model):
    security = models.CharField(max_length=50, default='none')
    network = models.CharField(max_length=50, default='tcp')
    tcp_settings = models.JSONField(default=dict)
    kcp_settings = models.JSONField(default=dict, blank=True, null=True)
    external_proxy = models.JSONField(default=list, blank=True, null=True)
    reality_settings = models.JSONField(default=dict, blank=True, null=True)
    xtls_settings = models.JSONField(default=dict, blank=True, null=True)
    tls_settings = models.JSONField(default=dict, blank=True, null=True)

class Client(models.Model):
    email = models.CharField(max_length=255)
    enable = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    method = models.CharField(max_length=50, default='chacha20-ietf-poly1305')
    sub_id = models.CharField(max_length=255, unique=True)
    tg_id = models.CharField(max_length=255, blank=True, null=True)
    total_gb = models.IntegerField(default=0)

    def __str__(self):
        return self.email

    
class Settings(models.Model):
    clients = models.ManyToManyField(Client)
    decryption = models.CharField(max_length=255, blank=True, null=True)
    fallbacks = models.JSONField(default=list, blank=True, null=True)

class Inbound(models.Model):
    remark = models.CharField(max_length=255, blank=False, null=False)
    enable = models.BooleanField(default=True)
    port = models.IntegerField()
    protocol = models.CharField(max_length=50, blank=True)
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE)
    stream_settings = models.OneToOneField(StreamSettings, on_delete=models.CASCADE)
    sniffing = models.OneToOneField(Sniffing, on_delete=models.CASCADE)
    up = models.BigIntegerField(default=0, blank=True)
    down = models.BigIntegerField(default=0, blank=True)
    total = models.BigIntegerField(default=0, blank=True)
    expiry_time = models.BigIntegerField(default=0, blank=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.remark


class UserClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'user')
    
    def __str__(self):
        return f"{self.user} -> {self.client}"