from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('gallery/<int:id>', views.gallery, name= 'gallery'),
    path('gallery/delete/<int:id>/', views.delete_gallery, name='delete_gallery'),
    path('gallery/<int:id>/download/', views.download_gallery, name='download_gallery'),
    path('edit-thumbnail/<int:thumbnail_id>/', views.edit_thumbnail, name='edit_thumbnail'),
    path('galleryform', views.galleryform, name= 'galleryform'),

    path('thumbnail/delete/<int:thumbnail_id>/', views.delete_thumbnail, name='delete_thumbnail'),
]