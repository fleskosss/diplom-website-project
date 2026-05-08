from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Profile: {self.user.username}'


class LeadRequest(models.Model):
    SOURCE_CONTACTS = 'contacts'
    SOURCE_ABOUT = 'about'
    SOURCE_SERVICES = 'services'
    SOURCE_AUTHOR_JEWELRY = 'author_jewelry'
    SOURCE_CHOICES = (
        (SOURCE_CONTACTS, 'Контакты'),
        (SOURCE_ABOUT, 'О нас'),
        (SOURCE_SERVICES, 'Услуги'),
        (SOURCE_AUTHOR_JEWELRY, 'Авторские украшения'),
    )

    source = models.CharField(max_length=30, choices=SOURCE_CHOICES)
    question = models.TextField()
    phone = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Lead #{self.pk} ({self.get_source_display()})'
