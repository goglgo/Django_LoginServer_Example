from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

GRADE_CHOICES = (
	('BRONZE', 'BRONZE'),
    ('SILVER', 'SILVER'),
    ('GOLD', 'GOLD'),
    ('PLATINUM', 'PLATINUM'),
    ('DIAMOND', 'DIAMOND'),
  )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    self_memo = models.TextField(max_length=100, blank=True)
    user_type = models.CharField(max_length=40, choices=GRADE_CHOICES, default=GRADE_CHOICES[0][0])
    
    def __str__(self):
        return self.user.username + ' / ' + self.user_type


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()