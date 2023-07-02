from django.core.files.uploadedfile import UploadedFile
from .models import Thumbnail, Gallery
from django import forms
from django.forms import inlineformset_factory
from PIL import Image
from io import BytesIO

class ThumbnailForm(forms.ModelForm):
    class Meta:
        model = Thumbnail
        fields = '__all__'

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if isinstance(image, UploadedFile):
            if not image.content_type.startswith('image'):
                raise forms.ValidationError("Only image files are allowed.")

            max_size = 2 * 1024 * 1024  # 2MB
            if image.size > max_size:
                raise forms.ValidationError("File size exceeds the limit of 2MB.")

            try:
                img = Image.open(image)

                if img.format != 'JPEG':
                    image_buffer = BytesIO()
                    img = img.convert('RGB')
                    img.save(image_buffer, format='JPEG', quality=90)

                    # Update the image field with the converted image
                    image = UploadedFile(image_buffer, image.name, 'image/jpeg')

            except Exception as e:
                raise forms.ValidationError("An error occurred while converting the image to JPEG format.")

        return image

GalleryFormSet = inlineformset_factory(
    Thumbnail,
    Gallery,
    form=ThumbnailForm,
    fields=('image',),
    extra=1,
    can_delete=False
)