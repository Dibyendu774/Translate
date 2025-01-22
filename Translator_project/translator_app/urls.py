from django.urls import path
from .views import *


urlpatterns = [
    path('', Home),
    path('text_translate', Google_T),
    path('image_translate', ImageTranslation)
]