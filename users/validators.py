from django.core.exceptions import ValidationError
import os

def file_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

def File_format(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def gif_format(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


