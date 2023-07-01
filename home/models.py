from django.db import models
import os
# Create your models here.

class Thumbnail(models.Model):
    title = models.CharField(max_length=50)
    thumbnail_image = models.ImageField(upload_to='thumbnail', max_length=255)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the associated gallery instances
        for gallery in self.galleries.all():
            gallery.delete()

        # Delete the thumbnail image file from the server
        if self.thumbnail_image:
            if os.path.exists(self.thumbnail_image.path):
                os.remove(self.thumbnail_image.path)

        # Call the superclass delete method to delete the record
        super().delete(*args, **kwargs)

class Gallery(models.Model):
    thumbnail = models.ForeignKey(Thumbnail,on_delete=models.CASCADE, related_name='galleries')
    image = models.ImageField(upload_to='gallery',max_length=255)

    def __str__(self):
        return self.thumbnail.title

    def delete(self, *args, **kwargs):
        # Delete the gallery image file from the server
        if self.image:
            if os.path.exists(self.image.path):
                os.remove(self.image.path)

        # Call the superclass delete method to delete the record
        super().delete(*args, **kwargs)