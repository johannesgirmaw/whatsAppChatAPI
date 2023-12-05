# chat/models.py

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def get_upload_path(instance, filename):
    # Customize the upload path based on content type
    return f'root/{instance.get_content_type_display()}/{filename}'

def validate_url(url):
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        raise ValidationError({"url": "Invalid Youtube URL"})
    
class CONTENT_TYPE(models.IntegerChoices):
    VIDEO = 100
    AUDIO = 101
    IMAGE = 102
    DOCUMENT = 103

def validate_file_extension(self, content_type, filename):
    # Define allowed extensions for each content type
    allowed_extensions = {
        CONTENT_TYPE.VIDEO: ("mp4", "avi", "wmv"),
        CONTENT_TYPE.AUDIO: ("mp3", "wav", "ogg"),
        CONTENT_TYPE.IMAGE: ("jpg", "jpeg", "png"),
        CONTENT_TYPE.DOCUMENT: ("pdf",),
    }
    extension = filename.split(".")[-1].lower()
    if extension not in allowed_extensions.get(content_type, ()):
        print(extension, allowed_extensions.get(content_type, ()))

        raise ValidationError({"url": f"Invalid file extension for {self.get_content_type_display()}"})

class Chatroom(models.Model):
    name = models.CharField(max_length=255)
    max_members = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    content = models.TextField()
    content_type = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    sender_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate content type
        super().clean()
        if self.content_type:
            validate_file_extension(self, self.content_type, self.content_type.name)

    @property
    def created_date(self):
        return self.timestamp

    def __str__(self):
        return self.content