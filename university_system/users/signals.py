from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User
import os

@receiver(pre_save,sender=User)
def delete_old_avatar(sender,instance,**kwargs):
    if not instance.pk:
        return False

    try:
        old_image = User.objects.get(id=instance.pk).avatar
    except User.DoesNotExist:
        return False
    
    new_image = instance.avatar
    if not new_image==old_image and old_image.filename!='default.png':
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)