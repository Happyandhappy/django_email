from django.db import models


class ClientEmails(models.Model):
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    html_content = models.TextField()
