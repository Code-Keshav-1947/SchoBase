from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)

    class Meta:
        ordering = ['-created_at'] # Hamesha latest notification upar dikhegi

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# Automation Signal Example: Jab bhi naya user join karega, notification create hogi
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def welcome_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            title="Welcome! 👋",
            message="Thank you for joining our platform. Check out your dashboard layout!"
        )