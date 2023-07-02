from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('gallery/<int:id>', GalleryView.as_view(), name='gallery'),
    path('galleryform', GalleryFormView.as_view(), name='galleryform'),
    path('gallery/delete/<int:id>/', GalleryDeleteView.as_view(), name='delete_gallery'),
    path('gallery/<int:id>/download/', DownloadGalleryView.as_view(), name='download_gallery'),
    path('edit-thumbnail/<int:thumbnail_id>/', EditThumbnailView.as_view(), name='edit_thumbnail'),
    path('thumbnail/delete/<int:thumbnail_id>/', ThumbnailDeleteView.as_view(), name='delete_thumbnail'),
]
