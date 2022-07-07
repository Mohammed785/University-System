from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os
from .models import Assignment, CourseFiles


@receiver(post_delete, sender=CourseFiles)
def delete_course_files(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(post_delete, sender=Assignment)
def delete_assignment_files(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(pre_save, sender=Assignment)
def delete_old_assignment(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = Assignment.objects.get(pk=instance.pk).file
    except Assignment.DoesNotExist:
        return False
    new_file = instance.file
    if not new_file == old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
