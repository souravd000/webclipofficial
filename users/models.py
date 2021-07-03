from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .validators import file_size, File_format
# Create your models here.


class profile(models.Model):
    Male = 'Male'
    FeMale = 'Female'
    Custom = 'Custom'
    Single = 'Single'
    Married = 'Married'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gif = models.FileField(default=False, upload_to='profile_gif')
    QR_Snap = models.ImageField(default='qrdefault.jpg', upload_to='QR_Snap')
    Bio = models.CharField(max_length=300, default='')
    website = models.URLField( blank=True)
    Birthday= models.CharField(max_length=100, default='')
    relations = ((Single, 'Single'), (Married, 'Married'))
    Relationship_status = models.CharField(max_length = 7, choices = relations, default='')
    Cover_Video = models.FileField(default='default.mp4', upload_to='cover_videos', validators=[file_size, File_format])
    GENDER_CHOICES = ((Male, 'Male'), (FeMale, 'FeMale'), (Custom, 'Custom'))
    Gender =  models.CharField(max_length = 6, choices = GENDER_CHOICES, default='')
    Location = models.CharField(max_length=100, blank=True)
    Payment_ID = models.CharField(max_length=200, blank=True)
    UPI_id = models.CharField(max_length=100, blank=True)
    Accepting_Contributions = models.BooleanField(default=False)
    Deactivate_Contributions = models.BooleanField(default=False)
    Messenger_ID = models.URLField(default='', blank=True)
    relationship_deactivate = models.BooleanField(default=False)
    gender_deactivate = models.BooleanField(default=False)
    Enable_page_setup = models.BooleanField(default=False)
    Page_activation = models.BooleanField(default=False)
    verify_account = models.BooleanField(default=False)
    vip_verify_account = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} profile'

