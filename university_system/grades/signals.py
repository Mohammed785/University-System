from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Grade, Semester,SemesterGrade, Year
from users.utils import get_current_semester,get_current_year

@receiver(pre_save,sender=Grade)
def create_semister(sender,instance,**kwargs):
    if not instance.pk:
        year,_ = Year.objects.get_or_create(year=get_current_year())
        semester,_ = Semester.objects.get_or_create(year=year,semester=get_current_semester())
        semester_grade = SemesterGrade.objects.get_or_create(student=instance.student,semester=semester)
        semester_grade.semester_grade_set.add(Grade)
        semester_grade.save()
    return