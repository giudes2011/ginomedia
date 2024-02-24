from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=40000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    def numberoflikes(self):
        return self.likes.count()
    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%d-%m-%Y %H:%M}): "
            f"{self.body}..."
            )
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name="seguito_da", symmetrical=False, blank=True)
    data_modificata = models.DateTimeField(User, auto_now=True)
    immagine_profilo = models.ImageField(null=True, blank=True, upload_to='img/')
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    # links to different social media platforms, cuz why not???
    facebook = models.CharField(null=True, blank=True, max_length=300)
    youtube = models.CharField(null=True, blank=True, max_length=500)
    instagram = models.CharField(null=True, blank=True, max_length=500)
    tiktok = models.CharField(null=True, blank=True, max_length=500)
    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created:
        profile.objects.get_or_create(user=instance)
