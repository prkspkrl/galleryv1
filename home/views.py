from django.shortcuts import render, get_object_or_404, redirect
from .forms import ThumbnailForm, GalleryFormSet
from .models import Thumbnail, Gallery
from django.http import HttpResponse
from django.views import View
import zipfile
import io

class HomeView(View):
    def get(self, request):
        thumb = Thumbnail.objects.all()
        context = {
            'thumb': thumb,
        }
        return render(request, 'home.html', context)

class GalleryView(View):
    def get(self, request, id):
        thumbnail = get_object_or_404(Thumbnail, id=id)
        galleries = thumbnail.galleries.all()
        context = {
            'thumbnail': thumbnail,
            'galleries': galleries,
        }
        return render(request, 'gallery.html', context)


class GalleryFormView(View):
    template_name = 'galleryform.html'
    def get(self, request, *args, **kwargs):
        thumbnail_form = ThumbnailForm()
        formset = GalleryFormSet(prefix='gallery_set')
        return render(request, self.template_name, {'thumbnail_form': thumbnail_form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        thumbnail_form = ThumbnailForm(request.POST, request.FILES)
        formset = GalleryFormSet(request.POST, request.FILES, prefix='gallery_set')
        if thumbnail_form.is_valid() and formset.is_valid():
            thumbnail = thumbnail_form.save()
            for form in formset:
                if form.cleaned_data.get('image'):
                    image = form.cleaned_data['image']
                    Gallery.objects.create(thumbnail=thumbnail, image=image)
            return redirect('home')
        return render(request, self.template_name, {'thumbnail_form': thumbnail_form, 'formset': formset})




class DownloadGalleryView(View):
    def get(self, request, id):
        thumbnail = get_object_or_404(Thumbnail, id=id)
        galleries = thumbnail.galleries.all()

        # Create an in-memory zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for gallery in galleries:
                image_path = gallery.image.path
                image_name = gallery.image.name
                zip_file.write(image_path, arcname=image_name)

        # Prepare the zip file for download
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="gallery_images.zip"'
        return response


class EditThumbnailView(View):
    def get(self, request, thumbnail_id):
        thumbnail = get_object_or_404(Thumbnail, pk=thumbnail_id)
        form = ThumbnailForm(instance=thumbnail)
        formset = GalleryFormSet(instance=thumbnail)
        return render(request, 'edit_thumbnail.html', {
            'form': form,
            'formset': formset,
            'thumbnail': thumbnail
        })

    def post(self, request, thumbnail_id):
        thumbnail = get_object_or_404(Thumbnail, pk=thumbnail_id)
        form = ThumbnailForm(request.POST, request.FILES, instance=thumbnail)
        formset = GalleryFormSet(request.POST, request.FILES, instance=thumbnail)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('home')

        return render(request, 'edit_thumbnail.html', {
            'form': form,
            'formset': formset,
            'thumbnail': thumbnail
        })




class GalleryDeleteView(View):
    def post(self, request, id):
        gallery = get_object_or_404(Gallery, id=id)
        thumbnail_id = gallery.thumbnail_id
        gallery.delete()
        return redirect('gallery', id=thumbnail_id)

class ThumbnailDeleteView(View):
    def get(self,request, thumbnail_id):
        thumbnail = get_object_or_404(Thumbnail, id=thumbnail_id)
        thumbnail.delete()
        return redirect('home')
