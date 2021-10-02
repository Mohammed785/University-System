from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from django.utils import timezone
from .managers import UserManager
from .utils import ID_generator,PathAndRename,image_resize

from datetime import date

class UserAbstract(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('Name'), max_length=50)
    email = models.EmailField(
        _('Email'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _('Email Is Already Exists')
        },
        validators=[EmailValidator(
            whitelist=['fci.helwan.edu.eg'])]
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.',
        )
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


GENDER_CHOICES = [
    ('M','Male'),
    ('F','Female')
]


rename_file = PathAndRename('images\\avatars')


class User(UserAbstract):
    en_name = models.CharField(verbose_name='English Name',max_length=40,null=True,blank=True)
    college_id = models.CharField(max_length=6, null=True, blank=True, unique=True, error_messages={'unique':'Please Enter Unique Email'})
    personal_email = models.EmailField(max_length=100, blank=True, null=True, unique=True, validators=[EmailValidator('Enter A valid Email', 'invalid', ['gmail', 'yahoo', 'hotmail', 'outlook'])], error_messages={'unique': 'Please Enter Unique Email'})
    birth_date = models.DateField(null=True,blank=True)
    mobile = models.CharField(max_length=12,null=True,blank=True)
    landline = models.CharField(max_length=12,null=True,blank=True)
    national_id = models.CharField(max_length=20,unique=True,null=True,blank=True) #make custom validator
    avatar = models.ImageField(upload_to=rename_file,default='images\\avatars\\default.png')
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)
    emergency_contact = models.CharField(max_length=12,null=True,blank=True)
    seat_number = models.PositiveSmallIntegerField(null=True,blank=True)
    is_prof = models.BooleanField(default=False)
    # is_student = models.BooleanField(default=False)

    class Meta(UserAbstract.Meta):
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return f'{self.name}' if self.is_prof else f'{self.name}/{self.college_id}' 

    @property
    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def get_contact_ways(self):
        return f"Mobile:{self.mobile}\nLandLine{self.landline}\nEmergency Contact:{self.emergency_contact}"

    @property
    def get_college_info(self):
        return f'Name:{self.name}\nID:{self.college_id}\nEmail:{self.email}'

    def save(self,*args,**kwargs):
        if not self.college_id:self.college_id = ID_generator(self)
        super().save(*args,**kwargs)
        image_resize(self.avatar.path)
