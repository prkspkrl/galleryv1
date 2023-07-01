from django.shortcuts import render, redirect
# Create your views here.
from .models import Thumbnail, Gallery
from .forms import ThumbnailForm, GalleryFormSet
from django.shortcuts import get_object_or_404

import io
import zipfile
from django.http import HttpResponse

def home(request):
    thumb = Thumbnail.objects.all()
    context = {
        'thumb': thumb,
    }
    return render(request, 'home.html', context)

def gallery(request, id):
    # galleries = Gallery.objects.filter(id=id)
    thumbnail = get_object_or_404(Thumbnail, id=id)
    galleries = thumbnail.galleries.all()
    context = {
        'thumbnail': thumbnail,
        'galleries': galleries,
    }
    return render(request, 'gallery.html', context)


def galleryform(request):
    if request.method == 'POST':
        thumbnail_form = ThumbnailForm(request.POST, request.FILES)
        formset = GalleryFormSet(request.POST, request.FILES)
        if thumbnail_form.is_valid() and formset.is_valid():
            thumbnail = thumbnail_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.thumbnail = thumbnail
                instance.save()
            return redirect('home')
    else:
        # print("this line")

        thumbnail_form = ThumbnailForm()
        formset = GalleryFormSet()


    context = {
        'thumbnail_form': thumbnail_form,
        'formset': formset,
    }
    return render(request, 'galleryform.html', context)



def download_gallery(request, id):
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



def edit_thumbnail(request, thumbnail_id):
    thumbnail = get_object_or_404(Thumbnail, pk=thumbnail_id)

    if request.method == 'POST':
        form = ThumbnailForm(request.POST, request.FILES, instance=thumbnail)
        formset = GalleryFormSet(request.POST, request.FILES, instance=thumbnail)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # Redirect to a success page or perform any other action
    else:
        form = ThumbnailForm(instance=thumbnail)
        formset = GalleryFormSet(instance=thumbnail)

    return render(request, 'edit_thumbnail.html', {
        'form': form,
        'formset': formset,
        'thumbnail': thumbnail
    })


def delete_gallery(request, id):
    gallery = get_object_or_404(Gallery, id=id)
    thumbnail_id = gallery.thumbnail_id
    gallery.delete()
    return redirect('gallery', id=thumbnail_id)

def delete_thumbnail(request, thumbnail_id):
    thumbnail = get_object_or_404(Thumbnail, id=thumbnail_id)
    thumbnail.delete()
    return redirect('home')