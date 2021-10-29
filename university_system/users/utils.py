from django.utils.deconstruct import deconstructible
from django.utils.crypto import get_random_string
from django.contrib import messages
from uuid import uuid4
from PIL import Image
from datetime import date
import os


def slug_generator(obj):
    slug = get_random_string(5)
    is_wrong = True
    while is_wrong:
        is_wrong = False
        obj_with_same_slug = type(obj).objects.filter(slug=slug)
        if len(obj_with_same_slug) > 0:
            is_wrong = True
            slug = get_random_string(5)
        else:
            return slug


def ID_generator(obj):
    college_d = get_random_string(6)
    is_wrong = True
    while is_wrong:
        is_wrong = False
        student_with_same_id = type(obj).objects.filter(college_id=college_d)
        if len(student_with_same_id) > 0:
            is_wrong = True
            college_d = get_random_string(6)
        else:
            return college_d


@deconstructible
class PathAndRename:
    def __init__(self, path) -> None:
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{ext}"
        return os.path.join(self.path, filename)


def image_resize(path):
    fixed_height = 720
    img = Image.open(path)
    if img.height > 720 or img.width > 1280:
        height_precent = fixed_height / float(img.size[1])
        width_size = int(float(img.size[0]) * float(height_precent))
        img = img.resize((width_size, fixed_height), Image.HAMMING)
        img.save(path)


def get_current_year():
    return date.today().year


def get_current_semester():
    month = date.today().month
    if month in [10, 11, 12, 1]:
        return "1ST"
    elif month in [3, 4, 5, 6]:
        return "2ND"


def delete_check(request, message, user):
    if not request.user == user and not request.user.is_prof:
        messages.warning(request, message)
        return False
