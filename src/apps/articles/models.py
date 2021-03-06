from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from django.utils.translation import gettext as _


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)


class Article(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_DECLINED = 'declined'

    STATUS_CHOICES = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_DECLINED, _('Declined'))
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255, verbose_name='Title', db_index=True)
    body = models.TextField(max_length=5000, verbose_name='Article body')
    tags = models.ManyToManyField(to='Tag', related_name='articles', blank=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    image = models.ImageField(upload_to='articles', null=True, blank=True)

    class Meta:
        permissions = [
            ('can_approve', 'Can approve'),
            ('can_decline', 'Can decline')
        ]


@receiver(models.signals.pre_save, sender=Article)
def upper_handler(sender, **kwargs):
    kwargs['instance'].body = kwargs['instance'].body.upper()
    # send_newsletters()
